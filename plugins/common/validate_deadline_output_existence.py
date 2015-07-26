import os

import pyblish.api


@pyblish.api.log
class ValidateDeadlineOutputExistence(pyblish.api.Validator):
    """Validates that the output directory for the write nodes exists"""

    families = ['deadline.render']
    version = (0, 1, 0)
    label = 'Output location existence'
    optional = True

    def process(self, instance):
        job_data = instance.data('deadlineJobData').copy()
        path, file = os.path.split(job_data['OutputFilename0'])
        if not os.path.exists(path):
            msg = 'Output directory for %s doesn\'t exists: %s' % (instance,
                                                                   path)
            raise ValueError(msg)

    def repair(self, instance):
        """Auto-repair creates the output directory"""
        job_data = instance.data('deadlineJobData').copy()
        path, file = os.path.split(job_data['OutputFilename0'])

        if not os.path.exists(path):
            os.makedirs(path)
