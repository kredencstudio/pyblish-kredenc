import pyblish.api


class CollectFtrackAssets(pyblish.api.Collector):

    """ Adds ftrack asset information to the instance
    """

    order = pyblish.api.Collector.order + 0.41
    label = 'Collect asset information'

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
                asset_name = ftrack_data['Task']['name']
                instance.data['ftrackAssetName'] = asset_name

            # task type filtering
            task_type = ftrack_data['Task']['type'].lower()
            asset_type = ''

            self.log.debug('task type {}'.format(task_type))

            if task_type == 'lighting':
                asset_type = 'scene'
            elif task_type == 'compositing':
                asset_type = 'comp'
            elif task_type == 'lookdev':
                asset_type = 'look'
            elif task_type == 'modeling':
                asset_type = 'geo'
            elif task_type == 'rigging':
                asset_type = 'rig'
            elif task_type == 'animation':
                asset_type = 'anim'
            elif task_type == 'fx':
                asset_type = 'fx'
            elif task_type == 'layout':
                asset_type = 'layout'

            families = instance.data['families']

            # family filtering
            if 'camera' in families:
                asset_type = 'cam'
            elif 'model' in families:
                asset_type = 'geo'
            elif 'cache' in families:
                asset_type = 'cache'
            elif 'scene' in families:
                asset_type = 'scene'
            elif 'review' in families:
                asset_type = 'mov'
            elif 'render' in families:
                asset_type = 'render'
                if 'writeNode' in families:
                    asset_type = 'img'

            if asset_type:
                instance.data['ftrackAssetType'] = asset_type
                self.log.debug('asset type: {}'.format(asset_type))

            self.log.debug('asset name: {}'.format(asset_name))
