# xUnit
[![Build Status](https://travis-ci.org/diegoguimaraes/xUnit.svg)](https://travis-ci.org/diegoguimaraes/xUnit)
[![Coverage Status](https://img.shields.io/coveralls/diegoguimaraes/xUnit.svg)](https://coveralls.io/r/diegoguimaraes/xUnit?branch=master)

Basic unit test framework for practice purposes, based on "Test-Driven Development by Example" by Kent Beck.

## Tests
Run the framework tests with `$ python -m xunit.test.tests`


## Usage example

Running all tests, `example.py`:

```Python
from xunit import TestCase

class TestExample(TestCase):

    def test_example(self):
        assert(1+1 == 2)

    def test_dummy(self):
        assert(2+2 == 4)
```

```bash
$ python -m xunit example
# 2 run, 0 failed
```

Running specific tests, `example.py`:

```Python
from xunit import TestCase, TestSuite, TestResult

class TestExample(TestCase):

    def test_example(self):
        assert(1+1 == 2)

    def test_dummy(self):
        assert(2+2 == 4)

suite = TestSuite()
suite.add(TestExample('test_example'))
result = TestResult()
suite.run(result)
print result.summary()

```

```sh
$ python example.py
# 1 run, 0 failed
$ python -m xunit example
# 1 run, 0 failed
```
