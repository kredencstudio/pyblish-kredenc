import shutil
import os
import pyblish.api
import pyblish_kredenc.utils as utils


@pyblish.api.log
class IntegrateMasterRig(pyblish.api.InstancePlugin):
    """Copies asset to it's final location
    """

    order = pyblish.api.IntegratorOrder
    # order = pyblish.api.ValidatorOrder
    families = ['scene']
    label = 'Master Rig'

    def process(self, instance):

        sourcePath = os.path.normpath(instance.context.data('currentFile'))
        self.log.debug(sourcePath)

        publishFile = instance.context.data('publishFile')
        self.log.debug(publishFile)

        vstring, version = utils.version_get(publishFile, 'v')
        self.log.debug(vstring + version)

        master_file = publishFile.replace('_{}{}'.format(vstring, version), '')
        self.log.debug('master file: {}'.format(master_file))

        shutil.copy(sourcePath, master_file)
