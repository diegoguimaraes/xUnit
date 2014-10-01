import sys
import inspect
import traceback


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
        except Exception:
            self.printExceptionMessage()
            result.test_failed()
        self.tearDown()

    def printExceptionMessage(self):
        print '{}'.format('='*60)
        print "FAIL: {}".format(self.name)
        print '{}'.format('-'*60)
        traceback.print_exc(file=sys.stdout)
        print '{}'.format('-'*60)

    def assertEquals(self, first, second):
        if not first == second:
            raise AssertionError("{} != {}".format(first, second))
        return True

    def assertNotEquals(self, first, second):
        if not first != second:
            raise AssertionError("{} == {}".format(first, second))
        return True

    def assertTrue(self, expression):
        if not expression:
            raise AssertionError("{} is not True".format(expression))
        return True

    def assertFalse(self, expression):
        if expression:
            raise AssertionError("{} is not False".format(expression))
        return True

    def assertIn(self, first, second):
        if first not in second:
            raise AssertionError("{} not in {}".format(first, second))
        return True

    def assertNotIn(self, first, second):
        if first in second:
            raise AssertionError("{} in {}".format(first, second))
        return True


class WasRun(TestCase):

    def __init__(self, name):
        TestCase.__init__(self, name)

    def test_method(self):
        self.was_run = 1
        self.log += "test_method "

    def tearDown(self):
        self.log += "tearDown "

    def broken_method(self):
        raise Exception("Expected test failure")


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

    def __init__(self, module=None, class_name=None, method_name=None):
        self._module = sys.modules['__main__'] if not module else module
        self.class_name = class_name
        self.method_name = method_name
        self.result = None

    def run(self, result):
        self.result = result
        if self.class_name and not self.method_name:
            self.run_all_class_methods()
        elif self.class_name and self.method_name:
            self.run_specified_method()
        else:
            self.run_all()

    def load_test_class(self):
        try:
            test_class = getattr(self._module, self.class_name)
        except AttributeError:
            return None
        return test_class

    def method_exists(self, class_name, method):
        try:
            getattr(class_name, method)
        except AttributeError:
            return False
        return True

    def run_all_class_methods(self):
        test_class = self.load_test_class()
        self.run_methods(test_class)

    def run_specified_method(self):
        test_class = self.load_test_class()
        if self.method_exists(test_class, self.method_name):
            test_class(self.method_name).run(self.result)

    def run_all(self):
        test_classes = self.get_classes_for_test()
        for test_class in test_classes.itervalues():
            self.run_methods(test_class)

    def run_methods(self, test_class):
        test_methods = self.get_class_methods(test_class)
        for method in test_methods.keys():
            test_class(method).run(self.result)

    def get_classes_for_test(self):
        classes = inspect.getmembers(self._module, inspect.isclass)
        classes = [i for i in classes if i[1].__module__ == self._module.__name__ and i[0].startswith('Test')]
        classes = [i for i in classes if issubclass(i[1], TestCase)]
        classes = dict(classes)
        return classes

    def get_class_methods(self, target_class):
        methods = inspect.getmembers(target_class, inspect.ismethod)
        methods = [m for m in methods if m[0].startswith('test')]
        methods = dict(methods)
        return methods
