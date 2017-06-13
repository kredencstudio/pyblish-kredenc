import os
import pyblish_kredenc.utils as pyblish_utils
import pyblish.api


@pyblish.api.log
class RepairOutputLocation(pyblish.api.Action):
    label = "Repair"
    on = "failed"
    icon = "wrench"

    def process(self, context, plugin):

        instances = pyblish_utils.filter_instances(context, plugin)
        for instance in instances:
            path, file = os.path.split(instance.data['outputFilename'])
            self.log.info(path)

            if not os.path.exists(path):
                self.log.info(path)
                os.makedirs(path)

@pyblish.api.log
class ValidateDeadlineOutputExistence(pyblish.api.InstancePlugin):
    """Validates that the output directory for the output exists"""

    order = pyblish.api.ValidatorOrder
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
