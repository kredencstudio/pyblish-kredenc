import pyblish.api

@pyblish.api.log
class CollectFtrackAsset(pyblish.api.Collector):

    """ Adds ftrack asset information to the instance
    """

    order = pyblish.api.Collector.order + 0.41
    label = 'Asset Attributes'

    def process(self, context):

        for instance in context:

            self.log.info('instance {}'.format(instance))
            # skipping instance if ftrackData isn't present
            if not context.has_data('ftrackData'):
                self.log.info('No ftrackData present. Skipping this instance')
                continue

            # skipping instance if ftrackComponents isn't present
            if not instance.has_data('ftrackComponents'):
                self.log.info('No ftrackComponents present\
                               Skipping this instance')
                continue

            ftrack_data = context.data['ftrackData'].copy()

            if not instance.data.get("ftrackAssetName"):
                instance.data['ftrackAssetName'] = ftrack_data['Task']['name']

            # task type filtering
            task_type = ftrack_data['Task']['type'].lower()
            asset_type = ''

            self.log.info('task type {}'.format(task_type))

            if task_type == 'lighting':
                asset_type = 'render'
            if task_type == 'compositing':
                asset_type = 'img'
            if task_type == 'lookdev':
                asset_type = 'look'
            if task_type == 'modeling':
                asset_type = 'geo'
            if task_type == 'rigging':
                asset_type = 'rig'
            if task_type == 'animation':
                asset_type = 'anim'

            # family filtering
            if 'camera' in instance.data['family']:
                asset_type = 'cam'
            if 'cache' in instance.data['family']:
                asset_type = 'cache'
            if 'render' in instance.data['family']:
                asset_type = 'render'

            if asset_type:
                instance.data['ftrackAssetType'] = asset_type
                self.log.info(instance.data['ftrackAssetType'])

            self.log.info(instance.data['ftrackAssetName'])
