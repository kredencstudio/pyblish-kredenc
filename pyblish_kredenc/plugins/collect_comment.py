import pyblish.api


class CollectComment(pyblish.api.Collector):
    """Adds comment section to GUI
    """

    order = pyblish.api.Collector.order
    label = 'Comment'

    def process(self, context):

        context.data["comment"] = ""

        self.log.info('Scene Version: %s' % context.data('version'))
