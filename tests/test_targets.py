def test_node_id_no_skip(base_tester):
    base_tester.makepyfile(
        """
        import pytest
        import os

        def test_a():
            pass

        @pytest.mark.regex_dependency('test_node_id_no_skip\.py::test_a')
        def test_b():
            pass

        class TestClass:
            def test_a(self):
                pass

        @pytest.mark.regex_dependency('test_node_id_no_skip\.py::TestClass::test_a')
        def test_c():
            pass

    """
    )

    result = base_tester.runpytest("--verbose")
    result.assert_outcomes(passed=4, skipped=0, failed=0)
    result.stdout.re_match_lines(
        r"""
        test_node_id_no_skip.py::test_a PASSED
        .*::test_b PASSED
        test_node_id_no_skip.py::TestClass::test_a PASSED
        .*::test_c PASSED
    """
    )


def test_node_id_skip(base_tester):
    base_tester.makepyfile(
        """
        import pytest
        import os

        def test_a():
            pytest.skip()

        @pytest.mark.regex_dependency('test_node_id_skip\.py::test_a')
        def test_b():
            pass

        class TestClass:
            def test_a(self):
                pytest.skip()

        @pytest.mark.regex_dependency('test_node_id_skip\.py::TestClass::test_a')
        def test_c():
            pass

    """
    )

    result = base_tester.runpytest("--verbose")
    result.assert_outcomes(passed=0, skipped=4, failed=0)
    result.stdout.re_match_lines(
        r"""
        test_node_id_skip.py::test_a SKIPPED
        .*::test_b SKIPPED
        test_node_id_skip.py::TestClass::test_a SKIPPED
        .*::test_c SKIPPED
    """
    )


def test_class_no_skip(base_tester):
    base_tester.makepyfile(
        """
        import pytest
        import os

        class TestClass:
            def test_a(self):
                pass

        @pytest.mark.regex_dependency('TestClass', target="class")
        def test_b():
            pass

    """
    )

    result = base_tester.runpytest("--verbose")
    result.assert_outcomes(passed=2, skipped=0, failed=0)
    result.stdout.re_match_lines(
        r"""
        .*::TestClass::test_a PASSED
        .*::test_b PASSED
    """
    )


def test_class_skip(base_tester):
    base_tester.makepyfile(
        """
        import pytest
        import os

        class TestClass:
            def test_a(self):
                pytest.skip()

        @pytest.mark.regex_dependency('TestClass', target="class")
        def test_b():
            pass

    """
    )

    result = base_tester.runpytest("--verbose")
    result.assert_outcomes(passed=0, skipped=2, failed=0)
    result.stdout.re_match_lines(
        r"""
        .*::TestClass::test_a SKIPPED
        .*::test_b SKIPPED
    """
    )


def test_module_no_skip(base_tester):

    base_tester.makepyfile(
        test_dependency="""
        import pytest
        import os

        def test_a():
            pass

        def test_b():
            pass

    """
    )

    base_tester.makepyfile(
        """
        import pytest
        import os

        @pytest.mark.regex_dependency('test_dependency\.py', target='module')
        def test_a():
            pass

    """
    )

    result = base_tester.runpytest("--verbose")
    result.assert_outcomes(passed=3, skipped=0, failed=0)
    result.stdout.re_match_lines(
        r"""
        test_dependency.py::test_a PASSED
        test_dependency.py::test_b PASSED
        test_module_no_skip.py::test_a PASSED
    """
    )


def test_module_skip(base_tester):

    base_tester.makepyfile(
        test_dependency="""
        import pytest
        import os

        def test_a():
            pass

        def test_b():
            pytest.skip()

    """
    )

    base_tester.makepyfile(
        """
        import pytest
        import os

        @pytest.mark.regex_dependency('test_dependency\.py', target='module')
        def test_a():
            pass

    """
    )

    result = base_tester.runpytest("--verbose")
    result.assert_outcomes(passed=1, skipped=2, failed=0)
    result.stdout.re_match_lines(
        r"""
        test_dependency.py::test_a PASSED
        test_dependency.py::test_b SKIPPED
        test_module_skip.py::test_a SKIPPED
    """
    )


def test_function_no_skip(base_tester):

    base_tester.makepyfile(
        test_dependency="""
        import pytest
        import os

        def test_a():
            pass

        def test_b():
            pass

    """
    )

    base_tester.makepyfile(
        """
        import pytest
        import os

        def test_a():
            pass

        @pytest.mark.regex_dependency('test_a', target='function')
        def test_b():
            pass

    """
    )

    result = base_tester.runpytest("--verbose")
    result.assert_outcomes(passed=4, skipped=0, failed=0)
    result.stdout.re_match_lines(
        r"""
        test_dependency.py::test_a PASSED
        test_dependency.py::test_b PASSED
        test_function_no_skip.py::test_a PASSED
        test_function_no_skip.py::test_b PASSED
    """
    )


def test_function_skip(base_tester):

    base_tester.makepyfile(
        test_dependency="""
        import pytest
        import os

        def test_a():
            pytest.skip()

        def test_b():
            pass

    """
    )

    base_tester.makepyfile(
        """
        import pytest
        import os

        def test_a():
            pass

        @pytest.mark.regex_dependency('test_a', target='function')
        def test_b():
            pass

    """
    )

    result = base_tester.runpytest("--verbose")
    result.assert_outcomes(passed=2, skipped=2, failed=0)
    result.stdout.re_match_lines(
        r"""
        test_dependency.py::test_a SKIPPED
        test_dependency.py::test_b PASSED
        test_function_skip.py::test_a PASSED
        test_function_skip.py::test_b SKIPPED
    """
    )
