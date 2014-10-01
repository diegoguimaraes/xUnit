import sys

from xunit import TestCase, WasRun, TestResult, TestSuite
from xunit import MainProgram


class TestCaseTest(TestCase):

    def setUp(self):
        self.result = TestResult()
        self.module = sys.modules[self.__module__]

    def test_template_method(self):
        test = WasRun('test_method')
        test.run(self.result)
        assert "setUp test_method tearDown " == test.log

    def test_result(self):
        test = WasRun('test_method')
        test.run(self.result)
        assert "1 run, 0 failed" == self.result.summary()

    def test_failed_result_formatting(self):
        self.result.test_started()
        self.result.test_failed()
        assert "1 run, 1 failed" == self.result.summary()

    def test_get_classes_for_test(self):
        suite = TestSuite(self.module)
        test_classes = suite.get_classes_for_test()
        assert self.__class__.__name__ in test_classes.keys()
        assert isinstance(self, test_classes[self.__class__.__name__])

    def test_if_classes_for_test_are_valid(self):
        suite = TestSuite(self.module)
        test_classes = suite.get_classes_for_test()
        assert 'TestInvalidClass' not in test_classes
        assert self.__class__.__name__ in test_classes

    def test_get_methods_for_test_in_each_class(self):
        suite = TestSuite(self.module)
        methods = suite.get_class_methods(TestCaseTest)
        assert 'test_template_method' in methods
        assert 'test_get_methods_for_test_in_each_class' in methods

    def test_if_test_methods_startswith_test(self):
        suite = TestSuite()
        methods = suite.get_class_methods(TestCaseTest)
        assert 'test_if_test_methods_startswith_test' in methods
        assert '__init__' not in methods

    def test_run_suite_with_specific_class_test(self):
        suite = TestSuite(self.module, 'MockTestClass')
        suite.run(self.result)
        assert "2 run, 0 failed" == self.result.summary()

    def test_run_suite_with_specific_inexistent_class(self):
        suite = TestSuite(self.module, 'Abc')
        suite.run(self.result)
        assert "0 run, 0 failed" == self.result.summary()

    def test_run_suite_with_specific_invalid_class(self):
        suite = TestSuite(self.module, 'TestInvalidClass')
        suite.run(self.result)
        assert "0 run, 0 failed" == self.result.summary()

    def test_run_suite_with_specific_class_and_method(self):
        suite = TestSuite(self.module, 'MockTestClass', 'test_dummy_sum')
        suite.run(self.result)
        assert "1 run, 0 failed" == self.result.summary()

    def test_run_suite_with_specific_class_and_inexistent_method(self):
        suite = TestSuite(self.module, 'MockTestClass', 'inexistent_method')
        suite.run(self.result)
        assert "0 run, 0 failed" == self.result.summary()


class TestInvalidClass:
    """This is an invalid test class.
    Test class must be a subclass of xunit.TestCase."""
    pass


class MockTestClass(TestCase):

    def test_dummy_sum(self):
        assert 1+2 == 3

    def test_dummy_multiply(self):
        assert 3*5 == 15


class TestMainProgram(TestCase):

    def test_if_module_string_is_empty(self):
        test_module = ''
        program = MainProgram(test_module)
        assert program.module is None

    def test_load_empty_module(self):
        program = MainProgram('')
        result = program.run()
        assert program.module is None
        assert result == "No module found."

    def test_load_invalid_module(self):
        program = MainProgram('invalid.module')
        result = program.run()
        assert program.module is None
        assert result == "No module found."

    def test_load_valid_module(self):
        program = MainProgram(self.__module__)
        assert program.module is not None

    def test_module_set_class_name(self):
        test_module = '{}.MockTestClass'.format(self.__module__)
        program = MainProgram(test_module)
        program.run()
        assert 'MockTestClass' == program.class_name

    def test_module_set_method_name(self):
        test_module = '{}.MockTestClass.test_dummy_sum'.format(self.__module__)
        program = MainProgram(test_module)
        program.run()
        assert 'test_dummy_sum' == program.method_name


class TestCaseAsserts(TestCase):

    def test_assert_equals(self):
        assert self.assertEquals(3, 3)
        try:
            assert self.assertEquals(2, 1)
        except AssertionError:
            pass

    def test_assert_not_equals(self):
        assert self.assertNotEquals(1, 2)
        try:
            assert self.assertNotEquals(2, 2)
        except AssertionError:
            pass

    def test_assert_true(self):
        assert self.assertTrue(1 == 1)
        try:
            assert self.assertTrue(1 == 2)
        except AssertionError:
            pass

    def test_assert_false(self):
        assert self.assertFalse(1 == 2)
        try:
            assert self.assertFalse(2 == 2)
        except AssertionError:
            pass

    def test_assert_in(self):
        assert self.assertIn('name', 'first name')
        assert self.assertIn(1, [3, 2, 1])
        try:
            assert self.assertIn(1, [3, 4, 5])
        except AssertionError:
            pass

    def test_assert_not_in(self):
        assert self.assertNotIn('George', 'John Smith')
        assert self.assertNotIn(1, [3, 4, 5])
        try:
            assert self.assertNotIn('key', {'key': 'some value'})
        except AssertionError:
            pass
