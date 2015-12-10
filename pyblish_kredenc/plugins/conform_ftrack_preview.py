import shutil
import os
import ftrack
import pyblish.api
from ft_studio import ft_pathUtils


@pyblish.api.log
class ConformFlipbook(pyblish.api.Conformer):
    """Copies Preview movie to it's final location

     Expected data members:
    'ftrackData' - Necessary ftrack information gathered by select_ftrack
    'outputPath' - Output path of current instance
    'version' - version of publish
    """

    families = ['preview']
    version = (0, 1, 0)
    label = 'Conform Preview'

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


            if 'Asset Build' not in parenttypes:
                templates = [
                    'shot.publish.file'
                ]
            else:
                templates = [
                    'asset.publish.file'
                ]

                self.log.debug(templates)
                publishFile = ft_pathUtils.getPathsYaml(task,
                                                        templateList=templates,
                                                        version=version)


                path, extension = os.path.splitext(publishFile[0])
                publishFile = path + ".mov"


            self.log.info('Moving preview from location: {}'.format(sourcePath))
            self.log.info('Moving preview to location: {}'.format(publishFile))
            shutil.move(sourcePath, publishFile)

            # ftrack data
            components = instance.data('ftrackComponents')
            components['preview']['path'] = publishFile

            instance.set_data('ftrackComponents', value=components)

        else:
            self.log.warning('preview wasn\'t created so it can\'t be published')
