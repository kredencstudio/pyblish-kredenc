import os

import pyblish.api


@pyblish.api.log
class ChechVersionLinking(pyblish.api.Validator):
    """Validates that the output directory for the write nodes exists"""

    families = ['deadline.render']
    version = (0, 1, 0)
    label = 'Check version linking'

    def process(self, instance, context):
        path = instance.data('deadlineOutput')

        if pyblish.api.current_host() != 'nuke':
            instance.set_data('ftrackVersionUsedID', value=context.data('ftrackData')['AssetVersion']['id'])

