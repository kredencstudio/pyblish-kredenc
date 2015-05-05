import pyblish.api

import nuke


@pyblish.api.log
class ValidateSceneSaved(pyblish.api.Validator):
    """Validates whether the scene is saved"""

    families = ['*']
    hosts = ['nuke']
    version = (0, 1, 0)

    def process_context(self, context):

        root = nuke.Root()
        if root.modified():
            msg = 'Scene has not been saved since modifying.'
            self.log.error(msg)
            raise pyblish.api.ValidationError('Scene has not been saved since modifying.'
                                              'this is how you fix it'
                                              'or like thos')

    def repair_context(self, context):
        """Saves the script
        """
        nuke.scriptSave()
