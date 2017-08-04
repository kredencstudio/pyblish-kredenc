import pyblish.api
from ftrack_kredenc import ft_pathUtils
reload(ft_pathUtils)


@pyblish.api.log
class ValidatePublishPathPack(pyblish.api.InstancePlugin):
    """Validates and attaches publishPath to assets

    Expected data members:
    'ftrackData' - Necessary frack information gathered by select_ftrack
    'version' - version of publish
    """
    order = pyblish.api.ValidatorOrder
    families = ['pack']
    label = 'Validate Packing Path'

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
                'shot.pack.file'
            ]
        else:
            templates = [
                'asset.pack.file'
            ]

        subset = ''
        if instance.data.get('subset'):
            subset = str(instance.data['subset'])

        if instance.data.get('item'):
            item = str(instance.data['item'])

        kwargs = {
            'family': instance.data['family'],
            'item': item,
            'version': version,
            'subset': subset,
            'ext': 'fbx'
            }

        self.log.debug(templates)
        self.log.debug(kwargs)
        publishFile = ft_pathUtils.getPathsYaml(taskid,
                                                templateList=templates,
                                                root=root,
                                                **kwargs
                                                )

        self.log.debug('paths returned: {}'.format(publishFile))
        # publishFile = publishFile[0]
        publishFile = 'K:/Projects/F002_king_of_sumava/sequences/a02/a02sh001/anim/publish/packs/kos_a02sh001_anim_v006/kos_a02sh001_anim_v006.fbx'
        instance.data['publishFile'] = publishFile
        self.log.debug('saving publishFile to instance: {}'.format(publishFile))

        # ftrack data
        # components = instance.data['ftrackComponents']
        # self.log.debug(str(components))
        # components = {instance.data['variation']: {'path': publishFile}}
        # self.log.debug(str(components))
        # instance.data['ftrackComponents'] = components
