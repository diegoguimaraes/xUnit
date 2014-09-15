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

    def test_suite_run_specific_methods(self):
        suite = TestSuite()
        suite.add(WasRun("test_method"))
        suite.add(WasRun("broken_method"))
        suite.run(self.result)
        assert("2 run, 1 failed" == self.result.summary())

    def test_get_classes_for_test(self):
        suite = TestSuite(self.module)
        test_classes = suite.get_classes_for_test()
        assert(self.__class__.__name__ in test_classes.keys())
        assert(isinstance(self, test_classes[self.__class__.__name__]))

    def test_if_classes_for_test_startswith_test(self):
        suite = TestSuite(self.module)
        test_classes = suite.get_classes_for_test()
        assert('NotValidTestClass' not in test_classes)
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


class NotValidTestClass:
    """This is an invalid test class. Test class must starts with 'Test' """
    pass


class TestMainProgram(TestCase):

    def test_command_line_module_argument_not_present(self):
        command_args = ['/home/diego/xunit/xunit/__main__.py']
        program = MainProgram(command_args)
        assert(program.module is None)

    def test_load_invalid_module(self):
        command_args = ['/home/diego/xunit/xunit/__main__.py', 'invalid.module']
        program = MainProgram(command_args)
        assert(program.module is None)

    def test_load_valid_module(self):
        command_args = ['/home/diego/xunit/xunit/__main__.py', 'xunit.test.tests']
        program = MainProgram(command_args)
        assert(program.module)

    def test_main_program_run(self):
        command_args = ['/home/diego/xunit/xunit/__main__.py']
        program = MainProgram(command_args)
        result = program.run()
        assert(result == "No module found.")
