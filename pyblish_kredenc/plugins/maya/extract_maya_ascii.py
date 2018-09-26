import os
import maya.cmds as mc
import pyblish_maya
import pyblish.api
import pyblish_kredenc.utils as pyblish_utils
from pyblish_kredenc.actions import actions_os

class ExtractMayaAscii(pyblish.api.Extractor):
    """Extract as Maya Ascii"""

    label = "Maya Ascii"
    hosts = ["maya"]
    families = ["model", 'camera', 'rig', 'look', 'location', 'prop']
    optional = True

    actions = [actions_os.OpenOutputFolder, actions_os.OpenOutputFile]

    def process(self, instance, context):
        self.log.info("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        # Define extract output file path
        dir_path = pyblish_utils.temp_dir(instance)
        filename = instance.name
        if not(filename.lower().endswith(".ma")):
            filename = filename + ".ma"

        path = os.path.join(dir_path, filename)

        self.log.info("{0}".format(path))

        #switch textures to proxty for better load times
        if context.data.get('ftrackData'):
            if context.data['ftrackData']['Project']['code'] == 'hbt':
                self.log.info("Switching texures to PROXY")
                import hbt_switch_tex as hbtSw
                reload(hbtSw)

                nhbtData=hbtSw.switchTexture()

                nhbtData.option = 2
                nhbtData.highest = False
                nhbtData.limit = 1600
                nhbtData.validatorCheck()
                nhbtData.fast = False

                if len(nhbtData.validatorSelection) > 0:
                    invalid = True

                nhbtData.all = True
                nhbtData.switch()

        # Perform extraction
        self.log.info("Performing extraction")
        # with pyblish_maya.maintained_selection():
        self.log.debug("instance: " + str(instance))
        roots = instance.data.get('roots')
        self.log.debug("roots: " + str(roots))
        if not roots:
            roots = instance
        mc.select(roots, noExpand=True)
        # mc.select(instance, noExpand=True)
        # self.log.info(instance.data['preserveReferences'])
        # preserveReferences = instance.data['preserveReferences'] or 'False'

        if instance.data['family'] in ['model', 'location']:

            path = mc.file(path,
                           es=True,
                           constructionHistory=False,
                           preserveReferences=False,
                           shader=True,
                           channels=False,
                           constraints=False,
                           force=True,
                           type='mayaAscii')

        elif instance.data['family'] in ['prop']:

           path = mc.file(path,
                          es=True,
                          constructionHistory=True,
                          preserveReferences=True,
                          shader=True,
                          channels=False,
                          constraints=True,
                          force=True,
                          type='mayaAscii')

        elif instance.data['family'] in ['rig', 'look', 'camera']:

            self.log.debug("EXTRACTING: " + str(instance))
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
