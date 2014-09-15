from xunit import TestSuite, TestResult


class MainProgram(object):

    def __init__(self, args):
        self.load_module(args)

    def load_module(self, args):
        module = None if len(args) == 1 else args[1]
        try:
            self.module = __import__(module, fromlist=['.'])
        except ImportError:
            self.module = None
        except TypeError:
            self.module = None

    def run(self):
        if not self.module:
            return 'No module found.'
        else:
            suite = TestSuite(self.module)
            result = TestResult()
            suite.run(result)
            return result.summary()
