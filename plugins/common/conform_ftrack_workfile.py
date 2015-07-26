import shutil
import os
import ftrack
import pyblish.api
import ft_pathUtils


@pyblish.api.log
class ConformWorkfile(pyblish.api.Conformer):
    """Copies current workfile to it's final location

    Expected data members:
    'ftrackData' - Necessary frack information gathered by select_ftrack
    'version' - version of publish
    """

    families = ['workFile']
    version = (0, 1, 0)
    label = 'Conform Workfile'

    def process(self, context, instance):
        sourcePath = os.path.normpath(context.data('currentFile'))

        publishFile = context.data('publishFile')

        shutil.copy(sourcePath, publishFile)

        # ftrack data
        components = instance.data('ftrackComponents')
        self.log.debug(str(components))
        if pyblish.api.current_host() == 'nuke':
            components['nukescript']['path'] = publishFile
        else:
            components['scene']['path'] = publishFile

        instance.set_data('ftrackComponents', value=components)

        self.log.info('Copying Workfile to location: {}'.format(publishFile))
