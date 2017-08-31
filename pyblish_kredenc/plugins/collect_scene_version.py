import os
import pyblish.api
import pyblish_kredenc.utils as pyblish_utils


class CollectSceneVersion(pyblish.api.Collector):
    """Finds version in the filename or uses the one found in the context
        Arguments:
        version (int, optional): version number of the publish
    """

    order = pyblish.api.Collector.order + 0.11
    label = 'Version'

    def process(self, context):

        filename = os.path.basename(context.data('currentFile'))

        # version data
        try:
            (prefix, version) = pyblish_utils.version_get(filename, 'v')
        except:
            self.log.warning('Cannot publish workfile which is not versioned.')
            return

        context.data['version'] = version
        context.data['vprefix'] = prefix

        self.log.info('Scene Version: %s' % context.data('version'))
