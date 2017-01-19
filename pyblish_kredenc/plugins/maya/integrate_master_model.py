import shutil
import os
import pyblish.api
import pyblish_kredenc.utils as utils


@pyblish.api.log
class IntegrateMasterModel(pyblish.api.InstancePlugin):
    """Copies asset to it's final location
    """

    order = pyblish.api.IntegratorOrder
    # order = pyblish.api.ValidatorOrder
    families = ['model']
    label = 'Master Model'
    optional = True

    def process(self, instance):

        extractedPaths = [v for k,v in instance.data.items() if k.startswith('outputPath')]
        self.log.debug(extractedPaths)
        for path in extractedPaths:

            sourcePath = path
            filename, ext = os.path.splitext(sourcePath)
            self.log.debug(sourcePath)

            publishFile = instance.data['publishFile']

            publishFile = os.path.splitext(publishFile)[0] + ext
            self.log.debug(publishFile)

            vstring, version = utils.version_get(publishFile, 'v')
            self.log.debug(vstring + version)

            master_file = publishFile.replace('_{}{}'.format(vstring, version), '')
            self.log.debug('master file: {}'.format(master_file))

            d = os.path.dirname(master_file)
            if not os.path.exists(d):
                os.makedirs(d)
            shutil.copy(sourcePath, master_file)
