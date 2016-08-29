import pyblish.api
from ft_studio import ft_pathUtils
reload(ft_pathUtils)


@pyblish.api.log
class ValidatePublishPathAssets(pyblish.api.InstancePlugin):
    """Validates and attaches publishPath to assets

    Expected data members:
    'ftrackData' - Necessary frack information gathered by select_ftrack
    'version' - version of publish
    """
    order = pyblish.api.ValidatorOrder
    families = ['model', 'rig', 'camera']
    label = 'Validate Asset Paths'

    def process(self, instance):

        version = instance.context.data['version']
        version = 'v' + str(version).zfill(3)
        self.log.debug(version)

        taskid = instance.context.data('ftrackData')['Task']['id']
        self.log.debug(taskid)

        root = instance.context.data('ftrackData')['Project']['root']
        self.log.debug(root)

        ftrack_data = instance.context.data['ftrackData']
        if 'Asset_Build' not in ftrack_data.keys():
            templates = [
                'shot.publish.item'
            ]
        else:
            templates = [
                'asset.publish.item'
            ]

        subset = ''
        if instance.data.get('subset'):
            subset = instance.data['subset']

        kwargs = {
                'family': instance.data['family'],
                'item': str(instance.data['item']),
                'version': version,
                'subset': subset,
                }

        self.log.debug(templates)
        self.log.debug(kwargs)
        publishFile = ft_pathUtils.getPathsYaml(taskid,
                                                templateList=templates,
                                                root=root,
                                                **kwargs
                                                )

        self.log.debug('paths returned: {}'.format(publishFile))
        publishFile = publishFile[0]
        instance.data['publishFile'] = publishFile
        self.log.debug('saving publishFile to instance: {}'.format(publishFile))

        # ftrack data
        # components = instance.data['ftrackComponents']
        # self.log.debug(str(components))
        # components = {instance.data['variation']: {'path': publishFile}}
        # self.log.debug(str(components))
        # instance.data['ftrackComponents'] = components
