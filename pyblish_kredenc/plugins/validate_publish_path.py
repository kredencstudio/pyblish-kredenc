import os
import pyblish.api
from ft_studio import ft_pathUtils
reload(ft_pathUtils)


@pyblish.api.log
class ValidatePublishPath(pyblish.api.Validator):
    """Validates that the publish directory for the workFile exists"""

    families = ['scene']
    version = (0, 1, 0)
    label = 'Publish Path'

    def process(self, context, instance):

        version = context.data['version']
        version = 'v' + str(version).zfill(3)
        self.log.debug(version)

        taskid = context.data('ftrackData')['Task']['id']
        self.log.debug(taskid)


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

        root = context.data('ftrackData')['Project']['root']
        self.log.debug(root)

        publishFiles = ft_pathUtils.getPathsYaml(taskid,
                                                 templateList=templates,
                                                 version=version,
                                                 root=root)

        publishFile = publishFiles[0]
        publishFolder = os.path.dirname(publishFile)
        self.log.debug(publishFile)

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
