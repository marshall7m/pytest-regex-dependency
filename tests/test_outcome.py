def test_valid_outcomes(base_tester):
    base_tester.makepyfile(
        """
        import pytest
        import os

        def test_a():
            pass

        @pytest.mark.regex_dependency('test_a', target="function", allowed_outcomes=["passed"])
        def test_b():
            pass

        @pytest.mark.regex_dependency('test_a', target="function", allowed_outcomes=["passed", "skipped"])
        def test_c():
            pass

        @pytest.mark.regex_dependency('test_a', target="function", allowed_outcomes=["passed", "failed"])
        def test_d():
            pass

        @pytest.mark.regex_dependency('test_a', target="function", allowed_outcomes=["passed", "skipped", "failed"])
        def test_e():
            pass
    """
    )

    result = base_tester.runpytest("--verbose")
    result.assert_outcomes(passed=5, skipped=0, failed=0)
    result.stdout.re_match_lines(
        r"""
        .*::test_a PASSED(?:\s+\(.*\))?
        .*::test_b PASSED(?:\s+\(.*\))?
        .*::test_c PASSED(?:\s+\(.*\))?
        .*::test_d PASSED(?:\s+\(.*\))?
        .*::test_e PASSED(?:\s+\(.*\))?
    """
    )


def test_invalid_outcomes(base_tester):
    base_tester.makepyfile(
        """
        import pytest
        import os

        def test_a():
            pass

        @pytest.mark.regex_dependency('test_a', target="function", allowed_outcomes=['skipped'])
        def test_b():
            pass

        @pytest.mark.regex_dependency('test_a', target="function", allowed_outcomes=["failed"])
        def test_c():
            pass

        @pytest.mark.regex_dependency('test_a', target="function", allowed_outcomes=["skipped", "failed"])
        def test_d():
            pass
    """
    )

    result = base_tester.runpytest("--verbose")
    result.assert_outcomes(passed=1, skipped=3, failed=0)
    result.stdout.re_match_lines(
        r"""
        .*::test_a PASSED(?:\s+\(.*\))?
        .*::test_b SKIPPED(?:\s+\(.*\))?
        .*::test_c SKIPPED(?:\s+\(.*\))?
        .*::test_d SKIPPED(?:\s+\(.*\))?
    """
    )
