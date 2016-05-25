import pyblish.api
import os
import pyblish_kredenc.utils as pyblish_utils


@pyblish.api.log
class CollectScene(pyblish.api.Collector):
    """Collects current workfile"""

    order = pyblish.api.Collector.order + 0.3
    label = 'Scene'

    def process(self, context):

        current_file = context.data('currentFile')
        directory, filename = os.path.split(str(current_file))
        self.log.info('current file: ' + current_file)

        patterns = ['.', 'untitled', 'root', 'untitled.hip']

        if any(pattern == filename.lower() for pattern in patterns):
            self.log.warning('New scene! Preparing an initial workfile')
            # create instance
            instance = context.create_instance(name='new_scene')
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

            instance.data['ftrackComponents'] = components
            self.log.info("Added: %s" % components)

            # version data
            try:
                (prefix, version) = pyblish_utils.version_get(filename, 'v')
            except:
                self.log.warning('Cannot publish workfile which is not versioned.')
                return


        if instance.data['family'] is not 'new_scene':
            if context.data['ftrackData']['Task']['type'] in [
                    'Modeling']:
                instance.data['publish'] = False

        context.data['version'] = version
        context.data['vprefix'] = prefix

        instance.add(current_file)
