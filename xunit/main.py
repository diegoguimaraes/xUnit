import xunit
from xunit import TestSuite, TestResult


class MainProgram(object):

    def __init__(self, test_module):
        self.test_module = test_module
        self.module = None
        self.module_class = None
        self.class_name = None
        self.method_name = None
        self.set_class_and_method_names()
        self.load_module()

    def set_class_and_method_names(self):
        module_path = self.test_module.split('.')
        if len(module_path) > 1:
            if module_path[-2][0].isupper() and module_path[-1].islower():
                self.class_name, self.method_name = module_path[-2], module_path[-1]
            elif module_path[-1][0].isupper():
                self.class_name = module_path[-1]
            else:
                self.class_name, self.method_name = None, None

    def load_module(self):
        if not self.test_module:
            return False
        else:
            self.module = self._import()

    def _import(self, string_module=None):
        string_module = string_module if string_module else self.test_module
        if string_module and self.class_name and self.class_name in string_module:
            string_module = string_module.partition(self.class_name)[0][:-1]
        try:
            module = __import__(string_module, fromlist=['.'])
        except (ImportError, ValueError):
            module = None
        return module

    def set_module_class(self):
        module = self.test_module.split('.')[:-1]
        module = '.'.join(map(str, module))
        module = self._import(module)
        try:
            module_class = getattr(module, self.class_name)
            self.module_class = module_class if issubclass(module_class, xunit.TestCase) else None
        except (AttributeError, TypeError):
            self.test_module_class = None

    def run(self):
        if not self.module:
            return 'No module found.'
        self.set_module_class()
        suite = TestSuite(self.module, self.class_name, self.method_name)
        result = TestResult()
        suite.run(result)
        return result.summary()
