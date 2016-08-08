import shutil
import os
import pyblish.api


@pyblish.api.log
class ConformScene(pyblish.api.Conformer):
    """Copies current workfile to it's final location

    Expected data members:
    'ftrackData' - Necessary frack information gathered by select_ftrack
    'version' - version of publish
    """

    families = ['scene']
    label = 'Scene'
    optional = True

    def process(self, instance):
        sourcePath = os.path.normpath(instance.context.data('currentFile'))
        self.log.debug(sourcePath)

        publishFile = instance.context.data('publishFile')
        self.log.debug(publishFile)

        shutil.copy(sourcePath, publishFile)

        # ftrack data
        components = instance.data('ftrackComponents')
        self.log.debug(str(components))

        if pyblish.api.current_host() == 'nuke':
            components = {'nukescript': {'path': publishFile}}
            # components['nukescript']['path'] = publishFile
        else:
            components = {'scene': {'path': publishFile}}
            # components['scene']['path'] = publishFile

        instance.set_data('ftrackComponents', value=components)
        self.log.info('Copying Workfile to location: {}'.format(publishFile))
