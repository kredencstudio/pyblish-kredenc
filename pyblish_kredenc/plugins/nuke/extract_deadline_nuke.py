import pyblish.api
import os

@pyblish.api.log
class ExtractDeadlineNuke(pyblish.api.Extractor):
    """ Gathers optional Nuke related data for Deadline
    """

    families = ['deadline']
    hosts = ['nuke']
    label = 'Nuke to Deadline'

    def process(self, instance):

        current_file = instance.context.data('currentFile')
        directory, filename = os.path.split(str(current_file))

        # getting deadline data
        job_data = {}
        plugin_data = {}
        if instance.has_data('deadlineData'):
            job_data = instance.data('deadlineData')['job'].copy()
            plugin_data = instance.data['deadlineData']['plugin'].copy()
        else:
            instance.data['deadlineData'] = {}

        # setting optional data
        job_data['Plugin'] = 'Nuke'
        job_data['Name'] = filename + " - " + instance.name
        job_data['UserName'] = instance.context.data['user']
        job_data['Frames'] = instance.data['frames']
        job_data['OutputFilename0'] = instance.data['outputFilename']

        job_data['Pool'] = 'comp'
        job_data['ChunkSize'] = '10'
        job_data['Group'] = 'nuke'
        job_data['LimitGroups'] = 'nuke'

        instance.data['deadlineData']['job'] = job_data

        plugin_data['SceneFile'] = instance.context.data['publishFile']
        plugin_data['WriteNode'] = instance.name
        plugin_data['BatchMode'] = 'True'
        plugin_data['EnforceRenderOrder'] = 'False'
        plugin_data['NukeX'] = 'False'
        plugin_data['Version'] = '11.2'

        instance.data['deadlineData']['plugin'] = plugin_data
