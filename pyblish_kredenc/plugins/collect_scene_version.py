import os

import pyblish.api
from pyblish_kredenc.utils import versioning


class CollectSceneVersion(pyblish.api.Collector):
    """Finds version in the filename or passes the one found in the context
        Arguments:
        version (int, optional): version number of the publish
    """

    order = pyblish.api.Collector.order + 0.1

    def process(self, context):

        filename = os.path.basename(context.data('currentFile'))

        prefix, version = versioning.version_get(filename, 'v')
        context.set_data('version', value=int(version))
        self.log.info('Scene Version: %s' % context.data('version'))

        context.set_data('vprefix', value=prefix)
