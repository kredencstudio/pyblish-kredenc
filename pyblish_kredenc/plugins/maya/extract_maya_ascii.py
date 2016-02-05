import os
import maya.cmds as mc
import pyblish_maya
import pyblish.api
import pyblish_kredenc.utils as pyblish_utils
reload(pyblish_utils)


class ExtractMayaAscii(pyblish.api.Extractor):
    """Extract as Maya Ascii"""

    label = "Maya Ascii"
    hosts = ["maya"]
    families = ["model", "rig", 'camera']
    optional = True

    def process(self, instance):

        # Define extract output file path
        dir_path = pyblish_utils.temp_dir(instance)
        filename = instance.name
        path = os.path.join(dir_path, filename)

        # Perform extraction
        self.log.info("Performing extraction..")
        with pyblish_maya.maintained_selection():
            self.log.info("instance.." + str(instance))
            mc.select(instance)
            # cmds.select(instance, noExpand=True)
            path = mc.file(path,
                           es=True,
                           constructionHistory=False,
                           preserveReferences=False,
                           shader=True,
                           channels=False,
                           constraints=False,
                           force=True,
                           type='mayaAscii')

            instance.data['outputPath_ma'] = path

        self.log.info("Extracted instance '{0}' to: {1}".format(
            instance.name, path))
