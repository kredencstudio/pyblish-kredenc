import pyblish.api
import ftrack


@pyblish.api.log
class CollectFtrackAsset(pyblish.api.Collector):

    """ Validate the existence of Asset, AssetVersion and Components.
    """

    order = pyblish.api.Collector.order + 0.41
    label = 'Collect Asset Attributes'

    def process(self, instance, context):

        # skipping instance if ftrackData isn't present
        if not context.has_data('ftrackData'):
            self.log.info('No ftrackData present. Skipping this instance')
            return

        # skipping instance if ftrackComponents isn't present
        if not instance.has_data('ftrackComponents'):
            self.log.info('No ftrackComponents present\
                           Skipping this instance')
            return

        ftrack_data = context.data('ftrackData').copy()

        if ftrack_data['Task']['code'] == 'light':
            instance.set_data('ftrackAssetType',
                              value='render')
            instance.set_data('ftrackAssetName',
                              value=ftrack_data['Task']['type'])
        if ftrack_data['Task']['code'] == 'comp':
            instance.set_data('ftrackAssetType',
                              value='comp')
            instance.set_data('ftrackAssetName',
                              value=ftrack_data['Task']['type'])
        if ftrack_data['Task']['code'] == 'lookdev':
            instance.set_data('ftrackAssetType',
                              value='img')
            instance.set_data('ftrackAssetName',
                              value=ftrack_data['Task']['type'])
