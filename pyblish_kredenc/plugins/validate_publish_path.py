import os
import pyblish.api
import sys

from ft_studio import ft_pathUtils
reload(ft_pathUtils)

import ftrack
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pyblish_utils


@pyblish.api.log
class ValidatePublishPath(pyblish.api.Validator):
    """Validates that the publish directory for the workFile exists"""

    families = ['scene']
    version = (0, 1, 0)
    label = 'Check Publish Path'

    def process(self, context, instance):

        sourcePath = os.path.normpath(context.data('currentFile'))
        directory, file = os.path.split(sourcePath)

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
                                                version=version)

        publishFile = publishFile[0]
        publishFolder = os.path.dirname(publishFile)
        self.log.debug(publishFolder)

        if os.path.exists(publishFolder):
            context.set_data('publishFile', value=publishFile)
            context.set_data('deadlineInput', value=publishFile)
            self.log.debug('Setting publishFile: {}'.format(publishFile))
        else:
            name = instance
            msg = 'Publish directory for %s doesn\'t exists' % name

            raise ValueError(msg)


    def repair(self, instance):
        """Auto-repair creates the output directory"""
        path = os.path.dirname(instance[0]['file'].value())

        if not os.path.exists(path):
            os.makedirs(path)
