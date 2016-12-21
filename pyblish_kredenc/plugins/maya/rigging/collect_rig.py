import pyblish.api
import os


@pyblish.api.log
class CollectRig(pyblish.api.Collector):
    """Collects current workfile"""

    order = pyblish.api.Collector.order
    label = 'Rig'

    def process(self, context):

        current_file = context.data('currentFile')
        directory, filename = os.path.split(str(current_file))
        self.log.info('current file: ' + current_file)


        # create instance
        instance = context.create_instance(name='control_rig')
        instance.data['family'] = 'rig'
        instance.data['families'] = ['rig']
        instance.data['path'] = current_file
        instance.data['item'] = 'control'

        self.log.warning('Collected instance: {}'.format(instance))

        # ftrack data
        components = {}
        components['ma'] = {'path': current_file}

        instance.data['ftrackComponents'] = components
        self.log.info("Added: %s" % components)

        instance.add(current_file)
