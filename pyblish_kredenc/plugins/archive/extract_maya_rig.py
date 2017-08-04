# import os
# import maya.cmds as mc
# import pyblish_maya
import pyblish.api
# import pyblish_kredenc.utils as pyblish_utils
from pyblish_kredenc.actions import actions_os

class ExtractRig(pyblish.api.Extractor):
    """Extract as Maya Ascii"""

    label = "Extract Rig"
    hosts = ["maya"]
    families = ["rig"]
    optional = True

    actions = [actions_os.OpenOutputFolder, actions_os.OpenOutputFile]

    def process(self, instance):

        # Define extract output file path
        # path = instance.data['path']

        # Perform extraction
        self.log.info("Performing extraction")

        instance.data['outputPath_ma'] = instance.data['path']
