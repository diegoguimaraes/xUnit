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
        assert("setUp test_method tearDown " == test.log)

    def test_result(self):
        test = WasRun('test_method')
        test.run(self.result)
        assert("1 run, 0 failed" == self.result.summary())

    def test_failed_result(self):
        test = WasRun('broken_method')
        test.run(self.result)
        assert("1 run, 1 failed" == self.result.summary())

    def test_failed_result_formatting(self):
        self.result.test_started()
        self.result.test_failed()
        assert("1 run, 1 failed" == self.result.summary())

    def test_get_classes_for_test(self):
        suite = TestSuite(self.module)
        test_classes = suite.get_classes_for_test()
        assert(self.__class__.__name__ in test_classes.keys())
        assert(isinstance(self, test_classes[self.__class__.__name__]))

    def test_if_classes_for_test_startswith_test(self):
        suite = TestSuite(self.module)
        test_classes = suite.get_classes_for_test()
        assert('InvalidTestClasss' not in test_classes)
        assert(self.__class__.__name__ in test_classes)

    def test_get_methods_for_test_in_each_class(self):
        suite = TestSuite(self.module)
        methods = suite.get_class_methods(TestCaseTest)
        assert('test_template_method' in methods)
        assert('test_get_methods_for_test_in_each_class' in methods)

    def test_if_test_methods_startswith_test(self):
        suite = TestSuite()
        methods = suite.get_class_methods(TestCaseTest)
        assert('test_if_test_methods_startswith_test' in methods)
        assert('__init__' not in methods)

    def test_run_suite_with_specific_class_test(self):
        test_module = sys.modules[self.__module__]
        class_name = 'MockTestClass'
        suite = TestSuite(test_module, class_name)
        suite.run(self.result)
        assert "2 run, 0 failed" == self.result.summary()


class InvalidTestClasss:
    """This is an invalid test class. Test class must be a subclass of xunit.TestCase."""
    pass


class MockTestClass(TestCase):

    def test_dummy_summ(self):
        assert 1+2 == 3

    def test_dummy_multiply(self):
        assert 3*5 == 15


class TestMainProgram(TestCase):

    def test_if_module_string_is_empty(self):
        test_module = ''
        program = MainProgram(test_module)
        assert program.module is None

    def test_if_test_module_has_valid_class(self):
        test_module_class = 'xunit.test.tests.%s' % self.__class__.__name__
        program = MainProgram(test_module_class)
        program.set_module_class()
        assert program.module_class is not None

    def test_if_test_module_has_invalid_class(self):
        test_module_class = 'xunit.test.tests.Abc'
        program = MainProgram(test_module_class)
        program.set_module_class()
        assert program.module_class is None

    def test_test_module_class_isnt_a_TestCase_subclass(self):
        test_module_class = 'xunit.test.tests.InvalidTestClasss'
        program = MainProgram(test_module_class)
        program.set_module_class()
        assert program.module_class is None

    def test_load_empty_module(self):
        test_module = ''
        program = MainProgram(test_module)
        result = program.run()
        assert program.module is None
        assert result == "No module found."

    def test_load_invalid_module(self):
        test_module = 'invalid.module'
        program = MainProgram(test_module)
        result = program.run()
        assert program.module is None
        assert result == "No module found."

    def test_load_valid_module(self):
        test_module = 'xunit.test.tests'
        program = MainProgram(test_module)
        assert program.module is not None
