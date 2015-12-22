import shutil
import os
import pyblish.api


@pyblish.api.log
class ConformAsset(pyblish.api.Conformer):
    """Copies asset to it's final location
    """

    families = ['model', 'rig']
    label = 'Conform Assets'

    def process(self, context, instance):

        extractedPaths = [v for k,v in instance.data.items() if k.startswith('outputPath')]
        for path in extractedPaths:

            # sourcePath = os.path.normpath(instance.data.get('outputPath'))
            sourcePath = path
            self.log.debug(sourcePath)
            filename, ext = os.path.splitext(sourcePath)
            publishFile = instance.data('publishFile')
            publishFile = os.path.splitext(publishFile)[0] + ext
            self.log.debug(publishFile)

            self.log.info('Copying model to location: {}'.format(publishFile))
            shutil.copy(sourcePath, publishFile)
