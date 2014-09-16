from xunit import TestSuite, TestResult


class MainProgram(object):

    def __init__(self, test_module):
        self.test_module = test_module
        self.load_module()

    def load_module(self):
        try:
            self.module = __import__(self.test_module, fromlist=['.'])
        except (ImportError, ValueError):
            self.module = None

    def run(self):
        if not self.module:
            return 'No module found.'
        suite = TestSuite(self.module)
        result = TestResult()
        suite.run(result)
        return result.summary()
