import pyblish.api

@pyblish.api.log
class ExtractDeadlineNuke(pyblish.api.Extractor):
    """ Gathers optional Nuke related data for Deadline
    """

    families = ['deadline.render']
    hosts = ['nuke']
    label = 'Nuke to Deadline'

    def process(self, instance):

        # getting job data
        job_data = {}
        if instance.has_data('deadlineData'):
            job_data = instance.data['deadlineData']['job'].copy()

        # setting optional data
        job_data['Pool'] = 'comp'
        job_data['ChunkSize'] = '10'
        group = 'nuke'
        job_data['Group'] = group
        job_data['LimitGroups'] = group

        instance.data['deadlineData']['job'] = job_data

        # getting plugin data
        plugin_data = {}
        if instance.has_data('deadlineData'):
            plugin_data = instance.data['deadlineData']['plugin'].copy()

        plugin_data['BatchMode'] = 'True'
        plugin_data['EnforceRenderOrder'] = 'False'
        plugin_data['NukeX'] = 'False'

        instance.data['deadlineData']['plugin'] = plugin_data
