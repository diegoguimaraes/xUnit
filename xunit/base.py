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
        except:
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

    def test_broken_method(self):
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

    def __init__(self):
        self.tests = []

    def add(self, test):
        self.tests.append(test)

    def run(self, result):
        for test in self.tests:
            test.run(result)
