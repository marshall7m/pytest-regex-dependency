def test_marker_registered(base_tester):
    result = base_tester.runpytest("--markers")
    result.stdout.fnmatch_lines(
        """
        @pytest.mark.regex_dependency*
    """
    )
