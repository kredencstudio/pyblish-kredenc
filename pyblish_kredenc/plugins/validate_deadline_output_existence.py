import os

import pyblish.api

class RepairOutputLocation(pyblish.api.Action):
    label = "Repair"
    on = "failed"
    icon = "wrench"

    def process(self, plugin, context):
        for instance in context:
            if instance.data['family'] == 'deadline.render':
                job_data = instance.data('deadlineData')['job'].copy()
                path, file = os.path.split(job_data['OutputFilename0'])

                if not os.path.exists(path):
                    os.makedirs(path)

@pyblish.api.log
class ValidateDeadlineOutputExistence(pyblish.api.Validator):
    """Validates that the output directory for the output exists"""

    families = ['deadline.render']
    label = 'Output location existence'
    hosts = ['nuke']
    optional = True
    actions = [RepairOutputLocation]

    def process(self, instance):
        job_data = instance.data('deadlineData')['job'].copy()
        path, file = os.path.split(job_data['OutputFilename0'])
        if not os.path.exists(path):
            msg = 'Output directory for %s doesn\'t exists: %s' % (instance,
                                                                   path)
            raise ValueError(msg)

    # def repair(self, instance):
    #     """Auto-repair creates the output directory"""
    #     job_data = instance.data('deadlineData')['job'].copy()
    #     path, file = os.path.split(job_data['OutputFilename0'])
    #
    #     if not os.path.exists(path):
    #         os.makedirs(path)
