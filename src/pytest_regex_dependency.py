import pytest
import logging
import sys
import re

log = logging.getLogger(__name__)
stream = logging.StreamHandler(sys.stdout)
log.addHandler(stream)
log.setLevel(logging.DEBUG)


def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "regex_dependency(pattern, target='node_id', allowed_outcomes=['passed']): "
        "mark a test to be used as a dependency for "
        "other tests or to depend on other tests.",
    )


def pytest_sessionstart(session):
    session.tracker = DependencyTracker()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    result = outcome.get_result()
    item.session.tracker.add(result)


def pytest_runtest_setup(item):
    """Check dependencies if this item is marked "dependency".
    Skip if any of the dependencies has not been run successnode_idy.
    """
    marker = item.get_closest_marker("regex_dependency")
    if marker is not None:
        if marker.args[0]:
            item.session.tracker.check(
                marker.args[0],
                marker.kwargs.get("target", "node_id"),
                marker.kwargs.get("allowed_outcomes", ["passed"]),
                item.name,
            )


class DependencyTracker(object):
    def __init__(self):
        self.results = {}

    def add(self, result):
        self.results.setdefault(result.nodeid, [])
        self.results[result.nodeid] += [result.outcome]

    def valid(self, nodeid, allowed_outcomes):
        outcomes = ["passed", "skipped", "failed"]
        invalid_outcomes = [out for out in outcomes if out not in allowed_outcomes]
        log.debug(f"Invalid outcomes: {invalid_outcomes}")
        log.debug(f"Outcomes: {self.results[nodeid]}")

        for out in invalid_outcomes:
            if out in self.results[nodeid]:
                return False
        return True

    def check(self, pattern, target, allowed_outcomes, test_name):
        if target == "node_id":
            log.debug(f"zozo: {self.results.items()}")
            for nodeid, outcome in self.results.items():
                if re.search(pattern, nodeid):
                    if self.valid(nodeid, allowed_outcomes):
                        log.debug(f"Dependency has expected outcomes: {nodeid}")
                    else:
                        pytest.skip(
                            f"Outcome for dependency: {nodeid} not expected  -- skipping test: {test_name}"
                        )


def regex_depends(
    self, request, pattern, target="node_id", allowed_outcomes=["passed"]
):
    """
    Add dependency on test
    """

    request.session.tracker.check(
        pattern,
        target,
        allowed_outcomes,
        request.node.name,
    )
