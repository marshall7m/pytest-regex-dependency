import pytest
import logging
import sys

pytest_plugins = [
    str("_pytest.pytester"),
]

log = logging.getLogger(__name__)
stream = logging.StreamHandler(sys.stdout)
log.addHandler(stream)
log.setLevel(logging.DEBUG)


@pytest.fixture
def base_tester(pytester):
    pytester.makeconftest(
        """
        import sys
        if "pytest_regex_dependency" not in sys.modules:
            pytest_plugins = "pytest_regex_dependency"
    """
    )
    return pytester
