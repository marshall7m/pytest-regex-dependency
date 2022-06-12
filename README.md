# pytest-regex-dependency
Management of Pytest dependencies via regex patterns


## Installation
```
pip install pytest-regex-dependency
```

## Use

The following examples are possible use cases for this plugin

- Test depends on tests with node Ids matching a specified pattern:

    `test_foo.py`
    ```
    import pytest
            

    def test_a():
        pass

    @pytest.mark.regex_dependency('test_foo\.py::test_a')
    def test_b():
        pass
    ```

- Test depends on all tests within module:

    `test_dependency.py`
    ```
    def test_a():
        pass

    def test_b():
        pass
    ```

    `test_bar.py`
    ```
    import pytest
            
    @pytest.mark.regex_dependency('test_dependency\.py', target='module')
    def test_a():
        pass
    ```

- Test depends on all tests within class:

    ```
    import pytest
            

    class TestClass:
        def test_a(self):
            pass

    @pytest.mark.regex_dependency('TestClass', target="class")
    def test_b():
        pass
    ```


- Test depends on all tests functions matching a specified pattern:

    ```
    import pytest
            

    def test_1():
        pass

    def test_2():
        pass

    def test_3():
        pass

    @pytest.mark.regex_dependency('test_[0-9]+$', target='function')
    def test_a():
        pass
    ```

## Considerations

- If a test's pattern is not met, the test function will run

    In the following example `test_b` will run:

    ```
    import pytest
            

    def test_a():
        pass

    @pytest.mark.regex_dependency('test_1')
    def test_b():
        pass
    ```

- The outcome of all phases of a dependency test is consider when determining if the calling test should be skipped. This includes the dependency test's setup, call, and teardown phases. If any of the phases do not match the calling test's `allowed_outcomes` requirement, the test will be skipped. This comes into light when a dependency test's fixture teardown logic fails but the dependency test succeeds.

    The following is an example of this scenario:
    ```
    import pytest
            

    @pytest.fixture
    def foo():
        yield None
        pytest.fail()

    def test_a(foo):
        pass

    @pytest.mark.regex_dependency('test_a', target="function", allowed_outcomes=["passed"])
    def test_b():
        pass
    ```