import sys
import inspect


class TestCase(object):

    def __init__(self, name):
        self.name = name

    def setUp(self):
        self.was_run = None
        self.log = "setUp "

    def tearDown(self):
        pass

    def run(self, result):
        result.test_started()
        self.setUp()
        try:
            method = getattr(self, self.name)
            method()
        except Exception, e:
            print(e.message)
            result.test_failed()
        self.tearDown()


class WasRun(TestCase):

    def __init__(self, name):
        TestCase.__init__(self, name)

    def test_method(self):
        self.was_run = 1
        self.log += "test_method "

    def tearDown(self):
        self.log += "tearDown "

    def broken_method(self):
        raise Exception


class TestResult(object):

    def __init__(self):
        self.run_count = 0
        self.error_count = 0

    def test_started(self):
        self.run_count += 1

    def test_failed(self):
        self.error_count += 1

    def summary(self):
        return "%s run, %s failed" % (self.run_count, self.error_count)


class TestSuite(object):

    def __init__(self, module=None):
        self._module = sys.modules['__main__'] if not module else module
        self.tests = []

    def add(self, test):
        self.tests.append(test)

    def run(self, result):
        if self.tests:
            self.run_specific_methods(result)
        else:
            self.run_all_methods(result)

    def run_specific_methods(self, result):
        for test in self.tests:
            test.run(result)

    def run_all_methods(self, result):
        test_classes = self.get_classes_for_test()
        for test_class in test_classes.itervalues():
            test_methods = self.get_class_methods(test_class)
            for method in test_methods.keys():
                test_class(method).run(result)

    def get_classes_for_test(self):
        classes = inspect.getmembers(self._module, inspect.isclass)
        classes = [i for i in classes if i[1].__module__ == self._module.__name__ and i[0].startswith('Test')]
        classes = dict(classes)
        return classes

    def get_class_methods(self, target_class):
        methods = inspect.getmembers(target_class, inspect.ismethod)
        methods = [m for m in methods if m[0].startswith('test')]
        methods = dict(methods)
        return methods
