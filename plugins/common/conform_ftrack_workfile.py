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

        # version = instance.context.data('version')
        # version = 'v' + str(version).zfill(3)
        #
        # taskid = instance.context.data('ftrackData')['Task']['id']
        # task = ftrack.Task(taskid)
        # parents = task.getParents()
        # # Prepare data for parent filtering
        # parenttypes = []
        # for parent in parents:
        #     try:
        #         parenttypes.append(parent.get('objecttypename'))
        #     except:
        #         pass
        # # choose correct template
        # if 'Episode' in parenttypes:
        #     templates = [
        #         'tv-ep-publish-file',
        #     ]
        # elif 'Sequence' in parenttypes:
        #     templates = [
        #         'tv-sq-publish-file',
        #     ]
        # elif 'Asset Build' in parenttypes:
        #     templates = [
        #         'tv-asset-publish-file',
        #     ]
        #
        # publishFile = ft_pathUtils.getPaths(taskid, templates, version)
        # publishFile = os.path.normpath(publishFile[templates[0]])

        shutil.copy(sourcePath, publishFile)

        # ftrack data
        components = instance.data('ftrackComponents')
        if pyblish.api.current_host() == 'nuke':
            components['nukescript']['path'] = publishFile
        else:
            components['scene']['path'] = publishFile

        instance.set_data('ftrackComponents', value=components)


        self.log.info('Copying Workfile to location: {}'.format(publishFile))

