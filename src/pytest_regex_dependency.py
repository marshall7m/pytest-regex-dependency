import pytest
import logging
import re

log = logging.getLogger(__name__)


def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "regex_dependency(pattern, target='node_id', allowed_outcomes=['passed']): "
        "Collects dependency tests that match the regex pattern and skips tests where"
        "the dependency tests don't meet the required outcomes",
    )


def pytest_sessionstart(session):
    session.tracker = DependencyTracker()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    result = outcome.get_result()
    item.session.tracker.add(result)


def pytest_runtest_setup(item):
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
        log.info(f"Adding {result.nodeid} outcome to dependency tracker")
        log.debug(f"\tPhase: {result.when}")
        log.debug(f"\tOutcome: {result.outcome}")

        self.results.setdefault(result.nodeid, [])
        self.results[result.nodeid] += [result.outcome]

    def valid(self, outcomes, allowed_outcomes):
        all_outcomes = ["passed", "skipped", "failed"]
        invalid_outcomes = [out for out in all_outcomes if out not in allowed_outcomes]
        log.debug(f"Invalid outcomes: {invalid_outcomes}")
        log.debug(f"Outcomes: {outcomes}")

        for out in invalid_outcomes:
            if out in outcomes:
                return False
        return True

    def check(self, pattern, target, allowed_outcomes, test_name):
        for nodeid, outcomes in self.results.items():
            if target == "node_id":
                target_match = re.search(pattern, nodeid)

            elif target == "module":
                target_match = re.search(pattern, nodeid.split("::")[0])

            elif target == "class":
                parsed_node_id = nodeid.split("::")
                if len(parsed_node_id) == 3:
                    target_match = re.search(pattern, nodeid.split("::")[1])
                else:
                    target_match = False

            elif target == "function":
                parsed_node_id = nodeid.split("::")
                if len(parsed_node_id) == 3:
                    target_match = re.search(pattern, nodeid.split("::")[2])
                else:
                    target_match = re.search(pattern, nodeid.split("::")[1])

            else:
                pytest.fail(f"target argument value is unknown: {target}")

            if target_match:
                log.debug(f"Checking dependency: {nodeid}")
                if self.valid(outcomes, allowed_outcomes):
                    log.debug(f"Dependency has expected outcomes: {nodeid}")
                else:
                    pytest.skip(
                        f"Outcome for dependency: {nodeid} not expected  -- skipping test: {test_name}"
                    )


def regex_depends(request, pattern, target="node_id", allowed_outcomes=["passed"]):

    request.session.tracker.check(
        pattern,
        target,
        allowed_outcomes,
        request.node.name,
    )
