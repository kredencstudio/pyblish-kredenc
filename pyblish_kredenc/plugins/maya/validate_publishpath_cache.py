import pyblish.api
from ft_studio import ft_pathUtils
reload(ft_pathUtils)


@pyblish.api.log
class ValidatePublishPathCache(pyblish.api.Validator):
    """Copies current workfile to it's final location

    Expected data members:
    'ftrackData' - Necessary frack information gathered by select_ftrack
    'version' - version of publish
    """

    families = ['cache']
    label = 'Validate Cache Paths'

    def process(self, instance):

        version = instance.context.data['version']
        version = 'v' + str(version).zfill(3)
        self.log.debug(version)

        taskid = instance.context.data('ftrackData')['Task']['id']
        self.log.debug(taskid)

        root = instance.context.data('ftrackData')['Project']['root']
        self.log.debug(root)

        ftrack_data = instance.context.data['ftrackData']
        if 'Asset_Build' in ftrack_data.keys():
            templates = [
            ]
        else:
            templates = [
                'shot.abccache.file'
            ]

        object_name = instance.data['name']

        self.log.debug(templates)
        publishFile = ft_pathUtils.getPathsYaml(taskid,
                                                templateList=templates,
                                                version=version,
                                                object_name=object_name,
                                                root=root)
        publishFile = publishFile[0]
        instance.data['publishFile'] = publishFile
        self.log.debug('saving publishFile to instance: {}'.format(publishFile))

        # ftrack data
        components = instance.data['ftrackComponents']
        self.log.debug(str(components))
        components[object_name]['path'] = publishFile
        self.log.debug(str(components))
        instance.data['ftrackComponents'] = components
