import pyblish.api

@pyblish.api.log
class ExtractDeadlineAss(pyblish.api.Extractor):
    """ Gathers optional Maya related data for Deadline
    """
    hosts = ['maya']
    families = ['deadline']
    label = 'Ass to Deadline'

    def process(self, instance):


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
        job_data['Group'] = 'maya_' + plugin_data['Version']

        instance.data['deadlineData']['job'] = job_data

        # setting plugin data
        scene = instance.context.data['publishFile']
        plugin_data['SceneFile'] = scene
        plugin_data['ProjectPath'] = scene
        plugin_data['ImageWidth'] = scene
        plugin_data['ImageHeight'] = scene
        plugin_data['OutputFilePath'] = scene
        plugin_data['OutputFilePrefix'] = scene
        plugin_data['Camera'] = scene
        plugin_data['Animation'] = scene

        instance.data['deadlineData']['plugin'] = plugin_data
