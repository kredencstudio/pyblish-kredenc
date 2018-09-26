import pyblish.api
from ftrack_kredenc import ft_utils
reload(ft_utils)


class ValidatePublishPathAssets(pyblish.api.InstancePlugin):
    """Validates and attaches publishPath to assets

    Expected data members:
    'ftrackData' - Necessary frack information gathered by select_ftrack
    'version' - version of publish
    """

    order = pyblish.api.ValidatorOrder
    families = ['model', 'rig', 'camera', 'look', 'cache', 'location', 'prop']
    label = 'Validate Asset Paths'

    def process(self, instance):

        version = instance.context.data['version']
        version = 'v' + str(version).zfill(3)
        taskid = instance.context.data('ftrackData')['Task']['id']
        root = instance.context.data('ftrackData')['Project']['root']

        subset = ''
        if instance.data.get('subset'):
            subset = instance.data['subset']

        kwargs = {
            'family': instance.data['family'],
            'item': str(instance.data['item']),
            'version': version,
            'subset': subset,
            }
        self.log.debug(kwargs)

        ftrack_data = instance.context.data['ftrackData']

        if 'Shot' in ftrack_data.keys():

            templates = ['shot.publish.item']
            self.log.debug(templates)
            publishFile = ft_utils.getPathsYaml(taskid,
                                                    templateList=templates,
                                                    root=root,
                                                    **kwargs
                                                    )[0]

            templates = ['shot.publish.master']
            self.log.debug(templates)
            masterFile = ft_utils.getPathsYaml(taskid,
                                                   templateList=templates,
                                                   root=root,
                                                   **kwargs
                                                   )[0]
        elif 'Asset_Build' in ftrack_data.keys():

            templates = ['asset.publish.item']
            self.log.debug(templates)
            publishFile = ft_utils.getPathsYaml(taskid,
                                                     templateList=templates,
                                                     root=root,
                                                     **kwargs
                                                     )[0]

            templates = ['asset.publish.master']
            self.log.debug(templates)
            masterFile = ft_utils.getPathsYaml(taskid,
                                                   templateList=templates,
                                                   root=root,
                                                   **kwargs
                                                   )[0]

        else:

            templates = ['folder.publish.item']
            self.log.debug(templates)
            publishFile = ft_utils.getPathsYaml(taskid,
                                                     templateList=templates,
                                                     root=root,
                                                     **kwargs
                                                     )[0]

            templates = ['folder.publish.master']
            self.log.debug(templates)
            masterFile = ft_utils.getPathsYaml(taskid,
                                                   templateList=templates,
                                                   root=root,
                                                   **kwargs
                                                   )[0]

        instance.data['publishFile'] = publishFile
        self.log.debug('publishFile data: {}'.format(publishFile))

        instance.data['masterFile'] = masterFile
        self.log.debug('masterFile data: {}'.format(masterFile))
