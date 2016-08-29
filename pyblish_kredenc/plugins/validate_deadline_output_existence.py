import os

import pyblish.api

class RepairOutputLocation(pyblish.api.Action):
    label = "Repair"
    on = "failed"
    icon = "wrench"

    def process(self, context, plugin):
        for instance in context:
            if instance.data['family'] == 'deadline':
                path, file = os.path.split(instance.data['outputFilename'])

                if not os.path.exists(path):
                    os.makedirs(path)

@pyblish.api.log
class ValidateDeadlineOutputExistence(pyblish.api.Validator):
    """Validates that the output directory for the output exists"""

    families = ['deadline']
    label = 'Output location existence'
    hosts = ['nuke']
    optional = True
    actions = [RepairOutputLocation]

    def process(self, instance):
        # job_data = instance.data('deadlineData')['job'].copy()
        path, file = os.path.split(instance.data['outputFilename'])
        if not os.path.exists(path):
            msg = 'Output directory for %s doesn\'t exists: %s' % (instance,
                                                                   path)
            raise ValueError(msg)
