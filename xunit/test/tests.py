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
        test = WasRun('test_broken_method')
        test.run(self.result)
        assert("1 run, 1 failed" == self.result.summary())

    def test_failed_result_formatting(self):
        self.result.test_started()
        self.result.test_failed()
        assert("1 run, 1 failed" == self.result.summary())

    def test_suite(self):
        suite = TestSuite()
        suite.add(WasRun("test_method"))
        suite.add(WasRun("test_broken_method"))
        suite.run(self.result)
        assert("2 run, 1 failed" == self.result.summary())

suite = TestSuite()
suite.add(TestCaseTest("test_template_method"))
suite.add(TestCaseTest("test_result"))
suite.add(TestCaseTest("test_failed_result"))
suite.add(TestCaseTest("test_failed_result_formatting"))
suite.add(TestCaseTest("test_suite"))
result = TestResult()
suite.run(result)
print result.summary()
