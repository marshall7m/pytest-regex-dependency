def test_valid_setup_outcome(base_tester):
    base_tester.makepyfile(
        """
        import pytest


        @pytest.fixture
        def foo():
            yield None

        def test_a(foo):
            pass

        @pytest.mark.regex_dependency('test_a', target="function", allowed_outcomes=["passed"])
        def test_b():
            pass
    """
    )

    result = base_tester.runpytest("--verbose")
    result.assert_outcomes(passed=2, skipped=0, failed=0)
    print(f"stderr: {result.stdout}")
    result.stdout.re_match_lines(
        r"""
        .*::test_a PASSED
        .*::test_b PASSED
    """
    )


def test_invalid_setup_outcome(base_tester):
    base_tester.makepyfile(
        """
        import pytest


        @pytest.fixture
        def foo():
            pytest.fail()
            yield None

        def test_a(foo):
            pass

        @pytest.mark.regex_dependency('test_a', target="function", allowed_outcomes=['passed'])
        def test_b():
            pass

        @pytest.mark.regex_dependency('test_a', target="function", allowed_outcomes=["skipped"])
        def test_c():
            pass

        @pytest.mark.regex_dependency('test_a', target="function", allowed_outcomes=["passed", "skipped"])
        def test_d():
            pass
    """
    )

    result = base_tester.runpytest("--verbose")
    result.assert_outcomes(passed=0, skipped=3, errors=1)
    result.stdout.re_match_lines(
        r"""
        .*::test_a ERROR
        .*::test_b SKIPPED
        .*::test_c SKIPPED
        .*::test_d SKIPPED
    """
    )


def test_valid_call_outcome(base_tester):
    base_tester.makepyfile(
        """
        import pytest


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


def test_invalid_call_outcome(base_tester):
    base_tester.makepyfile(
        """
        import pytest


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


def test_valid_teardown_outcome(base_tester):
    base_tester.makepyfile(
        """
        import pytest


        @pytest.fixture
        def foo():
            yield None
            pytest.skip()

        def test_a(foo):
            pass

        @pytest.mark.regex_dependency('test_a', target="function", allowed_outcomes=["skipped", "passed"])
        def test_b():
            pass
    """
    )

    result = base_tester.runpytest("--verbose")
    result.assert_outcomes(passed=2, skipped=1, failed=0)
    result.stdout.re_match_lines(
        r"""
        .*::test_a PASSED
        .*::test_a SKIPPED
        .*::test_b PASSED
    """
    )


def test_invalid_teardown_outcome(base_tester):
    base_tester.makepyfile(
        """
        import pytest


        @pytest.fixture
        def foo():
            yield None
            pytest.fail()

        def test_a(foo):
            pass

        @pytest.mark.regex_dependency('test_a', target="function", allowed_outcomes=['passed'])
        def test_b():
            pass

        @pytest.mark.regex_dependency('test_a', target="function", allowed_outcomes=["skipped"])
        def test_c():
            pass

        @pytest.mark.regex_dependency('test_a', target="function", allowed_outcomes=["passed", "skipped"])
        def test_d():
            pass
    """
    )

    result = base_tester.runpytest("--verbose")
    result.assert_outcomes(passed=1, skipped=3, errors=1)
    result.stdout.re_match_lines(
        r"""
        .*::test_a PASSED
        .*::test_a ERROR
        .*::test_b SKIPPED
        .*::test_c SKIPPED
        .*::test_d SKIPPED
    """
    )
