from teamcity.unittestpy import TeamcityTestResult
from teamcity.unittestpy import TeamcityTestRunner
from . import dom


class CyanTestResult(TeamcityTestResult):

    def __init__(self, stream, descriptions=None, verbosity=None):
        super(CyanTestResult, self).__init__(stream, descriptions, verbosity)

    def report_fail(self, test, fail_type, err):

        if not isinstance(test, str):
            file_name = test._testMethodName
            folder_name = self.get_directory_structure(test)
            dom.screen_shot(file_name, folder_name)

        super(CyanTestResult, self).report_fail(test, fail_type, err)

    def get_directory_structure(self, test) -> str:
        values = super(CyanTestResult, self).get_test_id(test).split(".")

        return "./Screenshots/{0}/{1}".format(values[0], values[1])


class CyanTestRunner(TeamcityTestRunner):
    resultclass = CyanTestResult

if __name__ == '__main__':
    from unittest import main

    main(module=None, testRunner=CyanTestRunner())
