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
        .*::test_a PASSED
        .*::test_b PASSED
        .*::test_c PASSED
        .*::test_d PASSED
        .*::test_e PASSED
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
        .*::test_a PASSED
        .*::test_b SKIPPED
        .*::test_c SKIPPED
        .*::test_d SKIPPED
    """
    )
