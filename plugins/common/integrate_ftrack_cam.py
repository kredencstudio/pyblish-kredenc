import shutil
import os
import ftrack
import pyblish.api
from ft_studio import ft_pathUtils


@pyblish.api.log
class IntegrateCamera(pyblish.api.Conformer):
    """Copies Preview movie to it's final location

     Expected data members:
    'ftrackData' - Necessary ftrack information gathered by select_ftrack
    'outputPath' - Output path of current instance
    'version' - version of publish
    """

    families = ['camera']
    hosts = ['houdini']
    version = (0, 1, 0)
    label = 'Conform Camera'

    def process(self, instance, context):

        if instance.has_data('outputPath'):
            sourcePath = os.path.normpath(instance.data('outputPath'))
            version = context.data('version')
            version = 'v' + str(version).zfill(3)

            taskid = context.data('ftrackData')['Task']['id']
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
                    'tv-ep-camera-file',
                ]
            elif 'Sequence' in parenttypes:
                templates = [
                    'tv-sq-camera-file',
                ]

            publishFile = ft_pathUtils.getPaths(task, templates, version)
            publishFile = os.path.normpath(publishFile[templates[0]])

            self.log.info('Copying preview to location: {}'.format(publishFile))
            shutil.copy(sourcePath, publishFile)

            # # ftrack data
            # components = instance.data('ftrackComponents')
            # components['preview']['path'] = publishFile

            # instance.set_data('ftrackComponents', value=components)

        else:
            self.log.warning('preview wasn\'t created so it can\'t be published')
