import pyblish.api

@pyblish.api.log
class ValidateVersionWorkfile(pyblish.api.Validator):
    """Validates whether workFile is versioned
    """

    families = ['scene']
    version = (0, 1, 0)
    label = 'Versioned File'

    def process(self, context):

        assert context.has_data('version'), 'Your workfile is not versioned!'
