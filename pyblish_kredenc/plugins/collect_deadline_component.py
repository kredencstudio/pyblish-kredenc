import pyblish.api

@pyblish.api.log
class CollectDeadlineComponent(pyblish.api.Selector):
    """Selects current workfile"""

    order = pyblish.api.Selector.order + 0.4
    version = (0, 1, 0)
    families = ['deadline.render']

    def process(self, instance, context):

        # ftrack data
        components = {}

        if pyblish.api.current_host() == 'nuke':
            try:
                components = {instance[0]['fcompname'].getValue(): {}}
                instance.set_data('ftrackComponents', value=components)
            except:
                components = {str(instance): {}}
                instance.set_data('ftrackComponents', value=components)
        else:
            if 'asset' in context.data('currentFile'):
                instance.set_data('ftrackAssetType', value='img')

            components = {str(instance): {}}
            instance.set_data('ftrackComponents', value=components)

        self.log.debug(str(components))
