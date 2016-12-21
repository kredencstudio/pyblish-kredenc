import os

import pyblish.api

@pyblish.api.log
class RepairOutputLocation(pyblish.api.Action):
    label = "Repair"
    on = "failed"
    icon = "wrench"

    def process(self, context):
        for instance in context:
            if instance.has_data('families'):
                if 'deadline' in instance.data['families']:
                    path, file = os.path.split(instance.data['outputFilename'])
                    self.log.info(path)

                    if not os.path.exists(path):
                        self.log.info(path)
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
