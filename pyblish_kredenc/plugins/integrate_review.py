import shutil
import os
import pyblish.api
from ft_studio import ft_pathUtils


@pyblish.api.log
class ConformFlipbook(pyblish.api.Conformer):
    """Copies Review movie to it's final location

     Expected data members:
    'ftrackData' - Necessary ftrack information gathered by select_ftrack
    'outputPath' - Output path of current instance
    'version' - version of publish
    """

    families = ['review']
    label = 'Review'

    def process(self, instance):

        extractedPaths = [v for k,v in instance.data.items() if k.startswith('outputPath')]

        componentPath = ''
        
        self.log.debug('Extracted Paths: {}'.format(extractedPaths))

        for sourcePath in extractedPaths:


            # sourcePath = os.path.normpath(instance.data('outputPath'))

            version = instance.context.data('version')
            version = 'v' + str(version).zfill(3)

            taskid = instance.context.data('ftrackData')['Task']['id']

            ftrack_data = instance.context.data['ftrackData']
            if 'Asset_Build' in ftrack_data.keys():
                templates = [
                    'asset.publish.scene'
                ]
            else:
                templates = [
                    'shot.publish.scene'
                ]

            self.log.debug(templates)
            root = instance.context.data('ftrackData')['Project']['root']
            self.log.debug(root)

            publishFile = ft_pathUtils.getPathsYaml(taskid,
                                                    templateList=templates,
                                                    version=version,
                                                    root=root)

            path, extension = os.path.splitext(publishFile[0])
            sourceFile, source_ext = os.path.splitext(sourcePath)

            publishFile = path + source_ext

            self.log.info('Moving preview from location: {}'.format(sourcePath))
            self.log.info('Moving preview to location: {}'.format(publishFile))
            shutil.move(sourcePath, publishFile)

            if '.mov' not in componentPath:
                componentPath = publishFile


        if componentPath:
            self.log.debug('Component Path: {}'.format(componentPath))
            components = instance.data['ftrackComponents'].copy()
            components['review']['path'] = componentPath


            instance.data['ftrackComponents'] = components

            self.log.debug('Components: {}'.format(instance.data['ftrackComponents']))
    #
        # else:
        #     self.log.warning('review wasn\'t created so it can\'t be published')
