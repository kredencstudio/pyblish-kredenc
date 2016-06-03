import pyblish.api

@pyblish.api.log
class ExtractDeadlineMaya(pyblish.api.Extractor):
    """ Gathers optional Maya related data for Deadline
    """
    hosts = ['maya']
    families = ['deadline.render']
    label = 'Maya to Deadline'

    def process(self, instance):

        if 'ass.render' in instance.data['families']:
            return

        # getting job data
        job_data = {}
        if instance.has_data('deadlineData'):
            job_data = instance.data('deadlineData')['job'].copy()

        # getting plugin data
        plugin_data = {}
        if instance.has_data('deadlineData'):
            plugin_data = instance.data['deadlineData']['plugin'].copy()

        # setting job data
        job_data['Pool'] = 'cg'
        job_data['LimitGroups'] = plugin_data['Renderer']
        job_data['Group'] = 'maya_' + plugin_data['Version'].replace('.', '_')

        instance.data['deadlineData']['job'] = job_data

        # setting plugin data
        scene = instance.context.data['publishFile']
        plugin_data['scene'] = scene

        instance.data['deadlineData']['plugin'] = plugin_data
