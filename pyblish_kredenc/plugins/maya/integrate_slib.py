import shutil
import os
import pyblish.api
import pyblish_kredenc.utils as utils


@pyblish.api.log
class IntegrateSlibRig(pyblish.api.InstancePlugin):
    """Copies asset to it's final location
    """

    order = pyblish.api.IntegratorOrder
    # order = pyblish.api.ValidatorOrder
    families = ['rig','model'] #,'model','look'z
    label = 'SLIB ANYTHING'
    optional = True

    def process(self, instance):
        validTypes = ['Modeling', 'Rigging']
        skip = True

        if instance.context.data.get('ftrackData'):
            asset = instance.context.data('ftrackData')['Asset_Build']['name']

            if instance.context.data['ftrackData']['Task']['type'] in validTypes:
                skip = False

        if not skip :
            sourcePath = os.path.normpath(instance.data['outputPath_ma'])
            self.log.debug('SLIB source file: {}'.format(sourcePath))

            publishFile = instance.data['publishFile']
            self.log.debug(publishFile)

            vstring, version = utils.version_get(publishFile, 'v')
            self.log.debug(vstring + version)

            root = instance.context.data('ftrackData')['Project']['root']

            asset = instance.context.data('ftrackData')['Asset_Build']['name']


            slib_folder = os.path.join(root, 'assets', 'lib', 'objects', instance.context.data['ftrackData']['Folder']['name'].capitalize(), asset.capitalize())
            if instance.data['item'] != 'main':
                slib_folder = os.path.join(root, 'assets', 'lib', 'objects', instance.context.data['ftrackData']['Folder']['name'].capitalize(), (asset.capitalize() + "_" + instance.data['item'].capitalize()))

            ext = os.path.splitext(publishFile)[1]

            slib_file = os.path.join(slib_folder, (asset + ext))
            if instance.data['item'] != 'main':
                slib_file = os.path.join(slib_folder, (asset + "_" + instance.data['item'].capitalize() + ext))
            self.log.debug('SLIB file: {}'.format(slib_file))

            if not os.path.exists(os.path.dirname(slib_file)):
                os.makedirs(os.path.dirname(slib_file))
            shutil.copy(sourcePath, slib_file)
