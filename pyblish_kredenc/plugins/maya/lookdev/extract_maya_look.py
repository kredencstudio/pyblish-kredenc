import os
import maya.cmds as mc
import pyblish_maya
import pyblish.api
import pyblish_kredenc.utils as pyblish_utils
from pyblish_kredenc.actions import actions_os

class ExtractMayaLook(pyblish.api.Extractor):
    """Extract as Maya Ascii"""

    label = "Extrack Look"
    hosts = ["maya"]
    families = ['look']
    optional = True

    actions = [actions_os.OpenOutputFolder, actions_os.OpenOutputFile]

    def process(self, instance):

        # Define extract output file path
        dir_path = pyblish_utils.temp_dir(instance)
        filename = instance.name
        path = os.path.join(dir_path, filename)

        # Perform extraction
        self.log.info("Performing extraction")
        with pyblish_maya.maintained_selection():
            self.log.debug("instance: " + str(instance))
            mc.select(instance)
            # cmds.select(instance, noExpand=True)
            # self.log.info(instance.data['preserveReferences'])
            # preserveReferences = instance.data['preserveReferences'] or 'False'

            path = mc.file(path,
                           es=True,
                           constructionHistory=True,
                           preserveReferences=True,
                           shader=True,
                           channels=True,
                           constraints=True,
                           force=True,
                           type='mayaAscii')

            instance.data['outputPath_ma'] = path

        self.log.info("Extracted instance '{0}' to: {1}".format(
            instance.name, path))
