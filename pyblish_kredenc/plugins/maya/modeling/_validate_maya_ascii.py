import shutil
import os
import pyblish.api
from ft_studio import ft_pathUtils
reload(ft_pathUtils)
import ftrack


@pyblish.api.log
class ValidatePublishPathAssets(pyblish.api.Validator):
    """Copies current workfile to it's final location

    Expected data members:
    'ftrackData' - Necessary frack information gathered by select_ftrack
    'version' - version of publish
    """

    families = ['model', 'rig']
    label = 'Validate Asset Paths'

    def process(self, context, instance):
        # sourcePath = os.path.normpath(instance.data.get('extractDir'))
        # assert sourcePath

        version = context.data['version']
        version = 'v' + str(version).zfill(3)
        self.log.debug(version)


        taskid = context.data('ftrackData')['Task']['id']
        self.log.debug(taskid)
        task = ftrack.Task(taskid)

        ftrack_data = context.data['ftrackData']
        if 'Asset_Build' not in ftrack_data.keys():
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
                                                version=version,
                                                object_name=instance.data['variation'])
        publishFile = publishFile[0]
        instance.data['publishFile'] = publishFile

        # shutil.copy(sourcePath, publishFile)
