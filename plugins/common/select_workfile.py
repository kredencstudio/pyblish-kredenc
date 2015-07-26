import pyblish.api
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pyblish_utils


@pyblish.api.log
class SelectWorkfile(pyblish.api.Selector):
    """Selects current workfile"""

    order = pyblish.api.Selector.order + 0.1
    version = (0, 1, 0)

    def process(self, context):

        current_file = context.data('currentFile')

        # set version
        directory, filename = os.path.split(current_file)

        # create instance
        instance = context.create_instance(name=filename)
        instance.set_data('family', value='workFile')
        instance.set_data('path', value=current_file)

        # ftrack data
        components = {}
        if pyblish.api.current_host() == 'nuke':
            components['nukescript'] = {'path': current_file}
        else:
            components['scene'] = {'path': current_file}
        instance.set_data('ftrackComponents', value=components)

        if 'asset' in current_file:
            instance.set_data('ftrackAssetType', value='img')

        # version data
        try:
            (prefix, version) = pyblish_utils.version_get(filename, 'v')
        except:
            self.log.warning('Cannot publish workfile which is not versioned.')
            return

        context.set_data('version', value=version)
        context.set_data('vprefix', value=prefix)

        instance.add(current_file)
