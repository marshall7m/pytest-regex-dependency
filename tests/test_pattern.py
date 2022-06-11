def test_node_id_no_skip(base_tester):
    base_tester.makepyfile(
        """
        import pytest
        import os

        def test_a():
            pass

        @pytest.mark.regex_dependency('test_node_id_no_skip\\.py::test_a')
        def test_b():
            pass

        @pytest.mark.regex_dependency('test_node_id_no_skip\\.py::test_b')
        def test_c():
            pass

    """
    )
    result = base_tester.runpytest("--verbose", "-s")
    result.assert_outcomes(passed=3, skipped=0, failed=0)
    result.stdout.re_match_lines(
        r"""
        .*::test_a PASSED(?:\s+\(.*\))?
        .*::test_b PASSED(?:\s+\(.*\))?
        .*::test_c PASSED(?:\s+\(.*\))?
    """
    )


def test_node_id_skip(base_tester):
    base_tester.makepyfile(
        """
        import pytest
        import os

        def test_a():
            pytest.skip()

        @pytest.mark.regex_dependency('test_node_id_skip\\.py::test_a')
        def test_b():
            pass

        @pytest.mark.regex_dependency('test_node_id_skip\\.py::test_b')
        def test_c():
            pass

    """
    )
    result = base_tester.runpytest("--verbose", "-s")
    result.assert_outcomes(passed=0, skipped=3, failed=0)
    result.stdout.re_match_lines(
        r"""
        .*::test_a SKIPPED(?:\s+\(.*\))?
        .*::test_b SKIPPED(?:\s+\(.*\))?
        .*::test_c SKIPPED(?:\s+\(.*\))?
    """
    )


def test_module_skip():
    pass


def test_class():
    pass


def test_function():
    pass
