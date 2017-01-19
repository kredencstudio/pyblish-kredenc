import pyblish.api
import os
import shutil
from pyblish_kredenc.actions import actions_os



class IntegrateAss(pyblish.api.InstancePlugin):
    """Integrates arnold archive files.
    """
    order = pyblish.api.IntegratorOrder
    families = ['arnold']
    optional = True

    actions = [actions_os.OpenPublishFolder]

    def process(self, instance):

        output_path = instance.data['outputPath_ass']
        self.log.debug('integrating outputPath: {}'.format(output_path))

        output_folder = os.path.split(output_path)[0]
        self.log.debug('integrating outputFolder: {}'.format(output_folder))

        publish_file = instance.data['publishFile']
        self.log.debug('integrating publishFile: {}'.format(publish_file))

        publish_folder = os.path.split(publish_file)[0]
        self.log.debug('integrating publishFolder: {}'.format(publish_folder))

        # if os.path.exists(publish_folder):
        #     self.log.debug('removing old path: {}'.format(publish_folder))
        #     # remove if exists
        #     shutil.rmtree(publish_folder)

        shutil.copytree(output_folder, publish_folder)
