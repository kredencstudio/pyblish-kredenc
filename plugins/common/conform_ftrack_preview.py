import shutil
import os
import ftrack
import pyblish.api
import ft_pathUtils


@pyblish.api.log
class ConformFtrackFlipbook(pyblish.api.Conformer):
    """Copies Preview movie to it's final location

     Expected data members:
    'ftrackData' - Necessary ftrack information gathered by select_ftrack
    'outputPath' - Output path of current instance
    'version' - version of publish
    """

    families = ['preview']
    hosts = ['*']
    version = (0, 1, 0)
    optional = True

    def process_instance(self, instance):

        if instance.has_data('outputPath'):
            sourcePath = os.path.normpath(instance.data('outputPath'))
            version = instance.context.data('version')
            version = 'v' + version

            ######################################################################################
            # TODO: figure out how to make path matching customisable
            ####

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
                    'tv-ep-preview-file',
                ]
            elif 'Sequence' in parenttypes:
                templates = [
                    'tv-sq-preview-file',
                ]

            publishFile = ft_pathUtils.getPaths(taskid, templates, version)
            publishFile = os.path.normpath(publishFile[templates[0]])

            ######################################################################################

            self.log.info('Copying preview to location: {}'.format(publishFile))
            shutil.copy(sourcePath, publishFile)
            instance.set_data('publishedFile', value=publishFile)

        else:
            self.log.warning('preview wasn\'t created so it can\'t be published')

