import os
import maya.cmds as mc
import pyblish_maya
import pyblish.api
import pyblish_kredenc.utils as pyblish_utils
from pyblish_kredenc.actions import actions_os

class ExtractMayaOBJ(pyblish.api.Extractor):
    """Extract as Maya OBJ"""

    label = "OBJ"
    hosts = ["maya"]
    families = ["model"]
    optional = True
    active = False

    actions = [actions_os.OpenOutputFolder, actions_os.OpenOutputFile]

    def process(self, instance):

        # Define extract output file path
        dir_path = pyblish_utils.temp_dir(instance)
        filename = instance.name
        path = os.path.join(dir_path, filename)

        # Perform extraction
        self.log.info("Performing extraction..")
        with pyblish_maya.maintained_selection():
            mc.select(instance)
            # cmds.select(instance, noExpand=True)
            path = mc.file(path,
                           es=True,
                           constructionHistory=False,
                           preserveReferences=False,
                           shader=False,
                           channels=False,
                           constraints=False,
                           force=True,
                           type='OBJexport')

            instance.data['outputPath_obj'] = path

        self.log.info("Extracted instance '{0}' to: {1}".format(
            instance.name, path))
