import pyblish.api
import os
import pyblish_kredenc.utils as pyblish_utils


@pyblish.api.log
class CollectScene(pyblish.api.Collector):
    """Selects current workfile"""

    order = pyblish.api.Collector.order + 0.1
    label = 'Scene'

    def process(self, context):

        current_file = context.data('currentFile')
        directory, filename = os.path.split(str(current_file))

        if current_file.lower() in ['', '.', 'untitled', 'root']:
            self.log.warning('New scene! Preparing an initial workfile')
            # create instance
            instance = context.create_instance(name=filename)
            instance.data['family'] = 'new_scene'
            instance.data['path'] = ''
            version = 1
            prefix = 'v'

        else:
            # create instance
            instance = context.create_instance(name=filename)
            instance.data['family'] = 'scene'
            instance.data['path'] = current_file

            self.log.warning('Collected instance: {}'.format(instance))
            self.log.warning('Scene path: {}'.format(current_file))

            # ftrack data
            components = {}
            if pyblish.api.current_host() == 'nuke':
                components['nukescript'] = {'path': current_file}
            else:
                components['scene'] = {'path': current_file}

            instance.set_data('ftrackComponents', value=components)
            self.log.info("Added: %s" % components)

            if 'asset' in str(current_file):
                instance.set_data('ftrackAssetType', value='img')

            # version data
            try:
                (prefix, version) = pyblish_utils.version_get(filename, 'v')
            except:
                self.log.warning('Cannot publish workfile which is not versioned.')
                return

        context.data['version'] = version
        context.data['vprefix'] = prefix

        instance.add(current_file)
