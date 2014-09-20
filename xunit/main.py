from xunit import TestSuite, TestResult


class MainProgram(object):

    def __init__(self, test_module):
        self.test_module = test_module
        self.module = None
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
                self.class_name, self.method_name = module_path[-1], None
            else:
                self.class_name, self.method_name = None, None

    def load_module(self):
        return self.import_module() if self.test_module else None

    def import_module(self, string_module=None):
        if self.test_module and self.class_name and self.class_name in self.test_module:
            self.test_module = self.test_module.partition(self.class_name)[0][:-1]
        try:
            self.module = __import__(self.test_module, fromlist=['.'])
        except (ImportError, ValueError):
            self.module = None

    def run(self):
        if not self.module:
            return 'No module found.'

        suite = TestSuite(self.module, self.class_name, self.method_name)
        result = TestResult()
        suite.run(result)
        return result.summary()
