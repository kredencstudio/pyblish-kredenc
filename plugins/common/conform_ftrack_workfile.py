import shutil
import os
import ftrack
import pyblish.api
import ft_pathUtils


@pyblish.api.log
class FtrackPublishWorkfile(pyblish.api.Conformer):
    """Copies current workfile to it's final location

    Expected data members:
    'ftrackData' - Necessary frack information gathered by select_ftrack
    'version' - version of publish
    """

    families = ['workFile']
    hosts = ['*']
    version = (0, 1, 0)
    optional = True

    def process_instance(self, instance):
        sourcePath = os.path.normpath(instance.context.data('currentFile'))

        ######################################################################################
        # TODO: figure out how to make path matching customisable
        ####

        version = instance.context.data('version')
        version = 'v' + version

        taskid = instance.context.data('ftrackData')['task']['id']
        task = ftrack.Task(taskid)
        parents = task.getParents()
        # Prepare data for parent filtering
        parenttypes = []
        for parent in parents:
            try:
                parenttypes.append(parent.get('objecttypename'))
            except:
                pass
        # choose correct template
        if 'Episode' in parenttypes:
            templates = [
                'tv-ep-publish-file',
            ]
        elif 'Sequence' in parenttypes:
            templates = [
                'tv-sq-publish-file',
            ]

        publishFile = ft_pathUtils.getPaths(taskid, templates, version)
        publishFile = os.path.normpath(publishFile[templates[0]])

        ###################################################################################

        self.log.info('Copying Workfile to location: {}'.format(publishFile))

        shutil.copy(sourcePath, publishFile)
        instance.set_data('publishedFile', value=publishFile)

