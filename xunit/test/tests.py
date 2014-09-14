from xunit import TestCase, WasRun, TestResult, TestSuite


class TestCaseTest(TestCase):

    def setUp(self):
        self.result = TestResult()

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
        suite = TestSuite()
        test_classes = suite.get_classes_for_test()
        assert(self.__class__.__name__ in test_classes.keys())
        assert(isinstance(self, test_classes[self.__class__.__name__]))

    def test_if_classes_for_test_startswith_test(self):
        suite = TestSuite()
        test_classes = suite.get_classes_for_test()
        assert('NotValidTestClass' not in test_classes)
        assert(self.__class__.__name__ in test_classes)

    def test_get_methods_for_test_in_each_class(self):
        suite = TestSuite()
        methods = suite.get_class_methods(TestCaseTest)
        assert('test_template_method' in methods)
        assert('test_get_methods_for_test_in_each_class' in methods)

    def test_if_test_methods_startswith_test(self):
        suite = TestSuite()
        methods = suite.get_class_methods(TestCaseTest)
        assert('test_if_test_methods_startswith_test' in methods)
        assert('__init__' not in methods)


class NotValidTestClass:
    """Test class must starts with Test"""
    pass

if __name__ == '__main__':
    suite = TestSuite()
    result = TestResult()
    suite.run(result)
    print(result.summary())
