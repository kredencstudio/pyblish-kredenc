import shutil
import os
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
    label = 'Preview'

    def process(self, instance, context):

        if instance.has_data('outputPath'):
            sourcePath = os.path.normpath(instance.data('outputPath'))

            version = context.data('version')
            version = 'v' + str(version).zfill(3)

            taskid = context.data('ftrackData')['Task']['id']

            ftrack_data = context.data['ftrackData']
            if 'Asset_Build' in ftrack_data.keys():
                templates = [
                    'asset.publish.file'
                ]
            else:
                templates = [
                    'shot.publish.file'
                ]

            self.log.debug(templates)
            root = context.data('ftrackData')['Project']['root']
            self.log.debug(root)
            publishFile = ft_pathUtils.getPathsYaml(taskid,
                                                    templateList=templates,
                                                    version=version,
                                                    root=root)

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
