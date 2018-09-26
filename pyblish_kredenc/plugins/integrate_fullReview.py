import shutil
import os
import pyblish.api
from ftrack_kredenc import ft_utils


@pyblish.api.log
class ConformFullFlipbook(pyblish.api.Conformer):
    """Copies Review movie to it's final location

     Expected data members:
    'ftrackData' - Necessary ftrack information gathered by select_ftrack
    'outputPath' - Output path of current instance
    'version' - version of publish
    """

    families = ['review']
    label = 'Full Review'
    optional = True
    active = True

    def process(self, instance):

        extractedPaths = [v for k,v in instance.data.items() if k.startswith('handleOutputPath')]

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

            publishFile = ft_utils.getPathsYaml(taskid,
                                                    templateList=templates,
                                                    version=version,
                                                    root=root)

            path, extension = os.path.splitext(publishFile[0])
            sourceFile, source_ext = os.path.splitext(sourcePath)

            publishFile = path + '_handle' + source_ext

            self.log.info('Moving full preview from location: {}'.format(sourcePath))
            self.log.info('Moving full preview to location: {}'.format(publishFile))

            d = os.path.dirname(publishFile)
            if not os.path.exists(d):
                os.makedirs(d)
            shutil.copy(sourcePath, publishFile)

            if '.mov' not in componentPath:
                componentPath = publishFile


        if componentPath:
            self.log.debug('Component Path: {}'.format(componentPath))
            components = instance.data['ftrackComponents'].copy()
            components['fullReview']['path'] = componentPath


            instance.data['ftrackComponents'] = components

            self.log.debug('Components: {}'.format(instance.data['ftrackComponents']))
    #
        # else:
        #     self.log.warning('review wasn\'t created so it can\'t be published')
