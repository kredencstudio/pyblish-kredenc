import os
import pyblish.api
import pyblish_kredenc.utils as pyblish_utils
from pyblish_kredenc.actions import actions_os


class RepairOutputPath(pyblish.api.Action):
    label = "Repair"
    on = "failed"
    icon = "wrench"

    def process(self, context, plugin):

        instances = pyblish_utils.filter_instances(context, plugin)

        for instance in instances:
            path = os.path.dirname(instance[0]['file'].value())

            if not os.path.exists(path):
                os.makedirs(path)


@pyblish.api.log
class ValidateOutputPath(pyblish.api.Validator):
    """Validates that the output directory for the instance exists"""

    families = ['writeNode', 'prerenders']
    hosts = ['nuke']
    label = 'Output Path'

    actions = [
        RepairOutputPath,
        actions_os.OpenOutputFolder,
        actions_os.OpenOutputFile
        ]

    def process(self, instance):
        name = instance[0].name()

        try:
            path = os.path.dirname(instance[0]['file'].value())
        except:
            path = None

        if path:
            if not os.path.exists(path):
                msg = 'Output directory for %s doesn\'t exists' % name
                self.log.error(msg)
                raise pyblish.api.ValidationError('You can run repair to create the directory automatically'
                                                  'or create it manually and re-run the publish')
        else:
            raise pyblish.api.ValidationError('No output directory could be found in %s, hence it can\'t be validated' % name)
