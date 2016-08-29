import os
import pyblish.api
from ft_studio import ft_pathUtils
reload(ft_pathUtils)
from pyblish_kredenc.actions import actions_os



class RepairPublishPath(pyblish.api.Action):
    label = "Repair"
    on = "failed"
    icon = "wrench"

    def process(self, context):

        path = os.path.dirname(context['publishFile'])

        if not os.path.exists(path):
            os.makedirs(path)


@pyblish.api.log
class ValidatePublishPath(pyblish.api.InstancePlugin):
    """Validates that the publish directory for the workFile exists"""

    order = pyblish.api.ValidatorOrder
    label = 'Publish Path'
    families = ['scene']

    actions = [
        RepairPublishPath,
        actions_os.OpenOutputFolder,
        actions_os.OpenOutputFile
        ]

    def process(self, instance):

        version = instance.context.data['version']
        version = 'v' + str(version).zfill(3)
        self.log.debug(version)

        taskid = instance.context.data('ftrackData')['Task']['id']
        self.log.debug(taskid)

        ftrack_data = instance.context.data['ftrackData']
        if 'Asset_Build' not in ftrack_data.keys():
            templates = [
                'shot.publish.scene'
            ]
        else:
            templates = [
                'asset.publish.scene'
            ]

        self.log.debug(templates)

        root = instance.context.data('ftrackData')['Project']['root']
        self.log.debug(root)

        publishFiles = ft_pathUtils.getPathsYaml(taskid,
                                                 templateList=templates,
                                                 version=version,
                                                 root=root)

        publishFile = publishFiles[0]
        publishFolder = os.path.dirname(publishFile)
        self.log.debug(publishFolder)

        if os.path.exists(publishFolder):
            instance.context.set_data('publishFile', value=publishFile)
            instance.context.data['deadlineInput'] = publishFile
            instance.data['outputPath_publish'] = publishFile
            self.log.debug('Setting publishFile: {}'.format(publishFile))
        else:
            name = instance
            msg = 'Publish directory for %s doesn\'t exists' % name

            raise ValueError(msg)
