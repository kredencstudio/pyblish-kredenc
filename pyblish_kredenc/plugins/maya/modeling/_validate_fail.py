import pyblish.api

class ValidateFail(pyblish.api.Validator):
    """ This plugin will fail"""

    optional = True
    active = False

    def process(self, instance):

        assert False, 'This plugin is designed to fail'
