import shutil
import pyblish.api
from ft_studio import ft_pathUtils
import os


@pyblish.api.log
class IntegrateCamera(pyblish.api.Conformer):
    """Copies camera to it's final location

     Expected data members:
    'ftrackData' - Necessary ftrack information gathered by select_ftrack
    'outputPath' - Output path of current instance
    'version' - version of publish
    """

    families = ['camera']
    version = (0, 1, 0)
    label = 'Camera'

    def process(self, instance):

        # Get Target Path
        version = instance.context.data('version')
        version = 'v' + str(version).zfill(3)

        taskid = instance.context.data('ftrackData')['Task']['id']

        root = instance.context.data('ftrackData')['Project']['root']
        self.log.debug(root)

        ftrack_data = instance.context.data['ftrackData']
        if 'Asset_Build' in ftrack_data.keys():
            templates = [
                'asset.cam.file'
            ]
        else:
            templates = [
                'shot.cam.file'
            ]

        publishFile = ft_pathUtils.getPathsYaml(taskid,
                                                templateList=templates,
                                                version=version,
                                                item='cam',
                                                root=root)[0]

        self.log.debug(publishFile)

        # Get source Path
        extractedPaths = [v for k,v in instance.data.items() if k.startswith('outputPath')]

        for path in extractedPaths:

            sourcePath = path
            self.log.debug(sourcePath)

            filename, ext = os.path.splitext(sourcePath)
            publishFile = os.path.splitext(publishFile)[0] + ext
            self.log.info('Copying camera to location: {}'.format(publishFile))

            shutil.copy(sourcePath, publishFile)
