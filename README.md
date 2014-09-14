# xUnit
[![Build Status](https://travis-ci.org/diegoguimaraes/xUnit.svg)](https://travis-ci.org/diegoguimaraes/xUnit)

Basic unit test framework for practice purposes, based on "Test-Driven Development by Example" by Kent Beck.

### Tests
Run the framework tests with `python xunit/test/tests.py`


### Usage example

```Python
from xunit import TestCase, TestSuite, TestResult

class TestExample(TestCase):

    def test_example(self):
        assert(1+1 == 2)

    def test_dummy(self):
        assert(2+2 == 4)
```

Run all tests:

```Python
suite = TestSuite()
result = TestResult()
suite.run(result)
print result.summary()

# 2 run, 0 failed
```

Run specific tests:

```Python
suite = TestSuite()
suite.add(TestExample('test_example'))
result = TestResult()
suite.run(result)
print result.summary()

# 1 run,  failed

```
