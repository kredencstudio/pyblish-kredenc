import pyblish.api
from ft_studio import ft_pathUtils
reload(ft_pathUtils)

class ValidatePublishPathCache(pyblish.api.InstancePlugin):
    """Copies current workfile to it's final location

    Expected data members:
    'ftrackData' - Necessary frack information gathered by select_ftrack
    'version' - version of publish
    """

    order = pyblish.api.ValidatorOrder
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
                'asset.abccache.file'
            ]
        else:
            templates = [
                'shot.abccache.file'
            ]

        subset = ''
        if instance.data.get('subset'):
            subset = instance.data['subset']

        item = instance.data['name']
        kwargs = {
                'family': instance.data['family'],
                'item': instance.data['item'],
                'version': version,
                'subset': subset,
                }

        self.log.debug(templates)
        publishFile = ft_pathUtils.getPathsYaml(taskid,
                                                templateList=templates,
                                                root=root,
                                                **kwargs
                                                )

        publishFile = publishFile[0]
        instance.data['publishFile'] = publishFile
        self.log.debug('saving publishFile to instance: {}'.format(publishFile))

        # ftrack data
        components = instance.data['ftrackComponents']
        self.log.debug(str(components))
        components[item]['path'] = publishFile
        self.log.debug(str(components))
        instance.data['ftrackComponents'] = components
