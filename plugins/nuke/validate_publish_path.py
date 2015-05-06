import os
import pyblish.api


@pyblish.api.log
class ValidatePublishPath(pyblish.api.Validator):
    """Validates that the publish directory for the workFile exists"""

    families = ['workFile']
    hosts = ['nuke']
    version = (0, 1, 0)
    optional = True

    def process_instance(self, instance):

        sourcePath = instance.data('path')
        directory, file = os.path.split(sourcePath)
        publishFolder = os.path.abspath(os.path.join(directory, '..', '_Publish'))
        publishFile = os.path.abspath(os.path.join(publishFolder, file))

        if os.path.exists(publishFolder):
            instance.context.set_data('published_scene_file', value=publishFile)
        else:
            name = instance
            msg = 'Publish directory for %s doesn\'t exists' % name

            raise ValueError(msg)

    def repair_instance(self, instance):
        """Auto-repair creates the output directory"""
        path = os.path.dirname(instance[0]['file'].value())

        if not os.path.exists(path):
            os.makedirs(path)
