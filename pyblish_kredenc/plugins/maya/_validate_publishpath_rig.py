import pyblish.api
from ftrack_kredenc import ft_pathUtils
reload(ft_pathUtils)


@pyblish.api.log
class ValidatePublishPathAssets(pyblish.api.Validator):
    """Copies current workfile to it's final location

    Expected data members:
    'ftrackData' - Necessary frack information gathered by select_ftrack
    'version' - version of publish
    """

    families = ['rig']
    label = 'Validate Asset Paths'

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

        object_name = None
        if instance.data.get('variation'):
            object_name = instance.data['variation']

        self.log.debug(templates)
        publishFile = ft_pathUtils.getPathsYaml(taskid,
                                                templateList=templates,
                                                version=version,
                                                object_name=object_name)
        publishFile = publishFile[0]
        instance.data['publishFile'] = publishFile
        self.log.debug('saving publishFile to instance: {}'.format(publishFile))

        # ftrack data
        components = instance.data['ftrackComponents']
        self.log.debug(str(components))
        components[instance.data['variation']]['path'] = publishFile
        self.log.debug(str(components))
        instance.data['ftrackComponents'] = components
