def test_depends_on_function_runtime(base_tester):
    base_tester.makepyfile(
        """
        import pytest
        from pytest_regex_dependency import regex_depends


        def test_a():
            pytest.skip()

        def test_b(request):
            regex_depends(request, 'test_a', target="function")

    """
    )

    result = base_tester.runpytest("--verbose")
    result.assert_outcomes(passed=0, skipped=2, failed=0)
    result.stdout.re_match_lines(
        r"""
        .*::test_a SKIPPED
        .*::test_b SKIPPED
    """
    )


def test_class_depends_on_function_runtime(base_tester):
    base_tester.makepyfile(
        """
        import pytest
        from pytest_regex_dependency import regex_depends


        def test_a():
            pytest.skip()

        class TestClass:
            def test_a(self, request):
                regex_depends(request, 'test_a', target="function")

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


def test_multiple_depends_runtime(base_tester):
    base_tester.makepyfile(
        """
        import pytest
        from pytest_regex_dependency import regex_depends


        def test_a():
            pytest.skip()

        def test_b():
            pass

        def test_c(request):
            regex_depends(request, 'test_a', target="function")
            regex_depends(request, 'test_b', target="function")

    """
    )

    result = base_tester.runpytest("--verbose")
    result.assert_outcomes(passed=1, skipped=2, failed=0)
    result.stdout.re_match_lines(
        r"""
        .*::test_a SKIPPED
        .*::test_b PASSED
        .*::test_c SKIPPED
    """
    )
