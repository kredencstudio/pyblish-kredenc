import shutil
import os
import pyblish.api
import pyblish_kredenc.utils as utils


@pyblish.api.log
class IntegrateSlibLook(pyblish.api.InstancePlugin):
    """Copies asset to it's final location
    """

    order = pyblish.api.IntegratorOrder
    # order = pyblish.api.ValidatorOrder
    families = ['look']
    label = 'SLIB Look'
    optional = True

    def process(self, instance):

        sourcePath = os.path.normpath(instance.data['outputPath_ma'])
        self.log.debug(sourcePath)

        publishFile = instance.data['publishFile']
        self.log.debug(publishFile)

        vstring, version = utils.version_get(publishFile, 'v')
        self.log.debug(vstring + version)

        root = instance.context.data('ftrackData')['Project']['root']

        asset = instance.context.data('ftrackData')['Asset_Build']['name']

        slib_folder = os.path.join(root, 'assets', 'lib', 'objects', 'Looks', asset)

        ext = os.path.splitext(publishFile)[1]

        slib_file = os.path.join(slib_folder, (asset + ext))

        self.log.debug('SLIB file: {}'.format(slib_file))

        if not os.path.exists(os.path.dirname(slib_file)):
            os.makedirs(os.path.dirname(slib_file))
        shutil.copy(sourcePath, slib_file)
