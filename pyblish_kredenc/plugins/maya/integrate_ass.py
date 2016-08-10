import pyblish.api
import pyblish_kredenc.utils as pyblish_utils
reload(pyblish_utils)
import os
import shutil
import pyblish_kredenc.plugins.actions_global as act
reload(act)


class IntegrateAss(pyblish.api.InstancePlugin):
    """Integrates arnold archive files.
    """
    order = pyblish.api.IntegratorOrder
    families = ['arnold']
    optional = True

    actions = [act.OpenPublishFolder]

    def process(self, instance):

        output_path = instance.data['outputPath_ass']
        self.log.debug('outputPath: {}'.format(output_path))

        output_folder = os.path.split(output_path)[0]
        self.log.debug('outputFolder: {}'.format(output_folder))

        publish_file = instance.data['publishFile']
        self.log.debug('publishFile: {}'.format(publish_file))

        publish_folder = os.path.split(publish_file)[0]
        self.log.debug('publishFolder: {}'.format(publish_folder))

        shutil.copytree(output_folder, publish_folder)
