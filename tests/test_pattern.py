def test_matched(base_tester):
    base_tester.makepyfile(
        """
        import pytest


        def test_a():
            pass

        # regex doesn't match anything see SO: https://stackoverflow.com/a/2930280/12659025
        @pytest.mark.regex_dependency('test_matched.py::test_a')
        def test_b():
            pass
    """
    )

    result = base_tester.runpytest("--verbose")
    result.assert_outcomes(passed=2, skipped=0, failed=0)
    result.stdout.re_match_lines(
        r"""
        .*::test_a PASSED
        .*::test_b PASSED
    """
    )


def test_not_matched(base_tester):
    base_tester.makepyfile(
        """
        import pytest


        def test_a():
            pass

        # regex doesn't match anything see SO: https://stackoverflow.com/a/2930280/12659025
        @pytest.mark.regex_dependency('\b\B')  # noqa: W605
        def test_b():
            pass
    """
    )

    result = base_tester.runpytest("--verbose")
    result.assert_outcomes(passed=2, skipped=0, failed=0)
    result.stdout.re_match_lines(
        r"""
        .*::test_a PASSED
        .*::test_b PASSED
    """
    )
