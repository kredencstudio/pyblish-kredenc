import shutil
import os
import pyblish.api
# import pyblish_kredenc.utils as utils


@pyblish.api.log
class IntegrateMasterCache(pyblish.api.InstancePlugin):
    """Copies asset to it's final location
    """

    order = pyblish.api.IntegratorOrder
    # order = pyblish.api.ValidatorOrder
    families = ['cache']
    label = 'Master Cache'
    optional = True

    def process(self, instance):

        sourcePath = os.path.normpath(instance.data['outputPath_abc'])
        filename, ext = os.path.splitext(sourcePath)
        self.log.debug(sourcePath)

        master_file = instance.data['masterFile']

        master_file = os.path.splitext(master_file)[0] + ext
        self.log.debug(master_file)

        master_file = master_file.replace('_{}{}'.format(vstring, version), '')
        self.log.debug('master file: {}'.format(master_file))

        shutil.copy(sourcePath, master_file)
