import pyblish.api

@pyblish.api.log
class ValidateVersionWorkfile(pyblish.api.Validator):
    """Validates whether workFile is versioned and makes sure that version number of write nodes matches version of the
    work file
    """

    families = ['workFile']
    hosts = ['*']
    version = (0, 1, 0)
    optional = True

    def process_instance(self, instance):

        if not instance.context.has_data('version'):
            msg = 'Your workfile is not versioned!'
            raise Exception(msg)
