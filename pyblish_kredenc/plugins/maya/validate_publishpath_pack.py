import pyblish.api
from ft_studio import ft_pathUtils
reload(ft_pathUtils)


@pyblish.api.log
class ValidatePublishPathPack(pyblish.api.Validator):
    """Validates and attaches publishPath to assets

    Expected data members:
    'ftrackData' - Necessary frack information gathered by select_ftrack
    'version' - version of publish
    """

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
            subset = instance.data['subset']

        kwargs = {
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
        publishFile = publishFile[0]
        instance.data['publishFile'] = publishFile
        self.log.debug('saving publishFile to instance: {}'.format(publishFile))

        # ftrack data
        # components = instance.data['ftrackComponents']
        # self.log.debug(str(components))
        # components = {instance.data['variation']: {'path': publishFile}}
        # self.log.debug(str(components))
        # instance.data['ftrackComponents'] = components
