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
        sourcePath = os.path.normpath(instance.data.get('extractDir'))
        self.log.debug(sourcePath)

        publishFile = instance.data('publishFile')
        self.log.debug(publishFile)

        self.log.info('Copying model to location: {}'.format(publishFile))
        shutil.copy(sourcePath, publishFile)

        # ftrack data
        components = instance.data['ftrackComponents']
        self.log.debug(str(components))
        components[instance.data['variation']]['path'] = publishFile
        self.log.debug(str(components))
        instance.data['ftrackComponents'] = components
