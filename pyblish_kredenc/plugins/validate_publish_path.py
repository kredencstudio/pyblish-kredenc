import os
import pyblish.api
from ft_studio import ft_pathUtils
reload(ft_pathUtils)
import pyblish_kredenc.plugins.actions_global as act
reload(act)


class RepairPublishPath(pyblish.api.Action):
    label = "Repair"
    on = "failed"
    icon = "wrench"

    def process(self, context):

        path = os.path.dirname(context['publishFile'])

        if not os.path.exists(path):
            os.makedirs(path)


@pyblish.api.log
class ValidatePublishPath(pyblish.api.Validator):
    """Validates that the publish directory for the workFile exists"""

    families = ['scene']
    version = (0, 1, 0)
    label = 'Publish Path'

    actions = [
        RepairPublishPath,
        act.OpenOutputFolder,
        act.OpenOutputFile
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
        self.log.debug(publishFile)

        if os.path.exists(publishFolder):
            instance.context.set_data('publishFile', value=publishFile)
            instance.context.data['deadlineInput'] = publishFile
            instance.data['outputPath_publish'] = publishFile
            self.log.debug('Setting publishFile: {}'.format(publishFile))
        else:
            name = instance
            msg = 'Publish directory for %s doesn\'t exists' % name

            raise ValueError(msg)
