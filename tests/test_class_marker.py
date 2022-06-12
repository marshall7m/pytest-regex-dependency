def test_class_depends_on_function(base_tester):
    base_tester.makepyfile(
        """
        import pytest


        def test_a():
            pytest.skip()

        @pytest.mark.regex_dependency('test_a', target="function")
        class TestClass:
            def test_a(self):
                pass

    """
    )

    result = base_tester.runpytest("--verbose")
    result.assert_outcomes(passed=0, skipped=2, failed=0)
    result.stdout.re_match_lines(
        r"""
        .*::test_a SKIPPED
        .*::TestClass::test_a SKIPPED
    """
    )


def test_class_depends_on_class(base_tester):
    base_tester.makepyfile(
        """
        import pytest



        class TestClassA:
            def test_a(self):
                pass

            def test_b(self):
                pytest.skip()

        @pytest.mark.regex_dependency('TestClassA', target="class")
        class TestClassB:
            def test_a(self):
                pass

            def test_b(self):
                pass

    """
    )

    result = base_tester.runpytest("--verbose")
    result.assert_outcomes(passed=1, skipped=3, failed=0)
    result.stdout.re_match_lines(
        r"""
        .*::TestClassA::test_a PASSED
        .*::TestClassA::test_b SKIPPED
        .*::TestClassB::test_a SKIPPED
        .*::TestClassB::test_b SKIPPED
    """
    )
