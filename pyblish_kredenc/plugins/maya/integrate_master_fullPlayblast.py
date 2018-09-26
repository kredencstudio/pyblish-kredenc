import shutil
import os
import pyblish.api
from ftrack_kredenc import ft_utils


@pyblish.api.log
class IntegrateFullEditReview(pyblish.api.InstancePlugin):
    """Copies Review movie to it's final location

    """

    order = pyblish.api.IntegratorOrder + 0.101
    families = ['review']
    label = 'Full Edit Review'
    optional = True

    def process(self, instance):

        if not 'Asset_Build' in instance.context.data['ftrackData']:


            extractedPaths = [v for k,v in instance.data.items() if k.startswith('handleOutputPath')]

            self.log.info('Doing the Integrate Edit Review')

            self.log.debug('Extracted Paths: {}'.format(extractedPaths))

            review_path = instance.data['ftrackComponents']['fullReview']['path']

            # for sourcePath in extractedPaths:


            # sourcePath = os.path.normpath(instance.data('outputPath'))
            sourceFile, source_ext = os.path.splitext(review_path)

            # if source_ext not in ['mov', 'mp4']:
            #     break

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
                    'shot.playblast.temp'
                ]

            self.log.debug(templates)
            root = instance.context.data('ftrackData')['Project']['root']
            self.log.debug(root)

            kwargs = {
                'codec': 'h264',
                }

            publishFile = ft_utils.getPathsYaml(taskid,
                                                templateList=templates,
                                                version=version,
                                                root=root,
                                                **kwargs
                                                )[0]


            path, extension = os.path.splitext(publishFile)
            publishFile = path + "_handle" + source_ext

            self.log.info('Copying EDIT FULL PREVIEW from location: {}'.format(review_path))
            self.log.info('Copying EDIT FULL PREVIEW to location: {}'.format(publishFile))

            d = os.path.dirname(publishFile)
            if not os.path.exists(d):
                os.makedirs(d)
            shutil.copy(review_path, publishFile)
            #
            # if '.mov' not in componentPath:
            #     componentPath = publishFile


        # if componentPath:
        #     self.log.debug('Component Path: {}'.format(componentPath))
        #     components = instance.data['ftrackComponents'].copy()
        #     components['review']['path'] = componentPath
        #
        #
        #     instance.data['ftrackComponents'] = components
        #
        #     self.log.debug('Components: {}'.format(instance.data['ftrackComponents']))
    #
        # else:
        #     self.log.warning('review wasn\'t created so it can\'t be published')
