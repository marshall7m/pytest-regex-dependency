import logging
import sys

log = logging.getLogger(__name__)
stream = logging.StreamHandler(sys.stdout)
log.addHandler(stream)
log.setLevel(logging.DEBUG)


def test_marker_registered(base_tester):
    result = base_tester.runpytest("--markers")
    result.stdout.fnmatch_lines(
        """
        @pytest.mark.regex_dependency*
    """
    )
