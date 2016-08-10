import pyblish.api
import os
import pymel

@pyblish.api.log
class ExtractDeadlineLayer(pyblish.api.InstancePlugin):
    """ Gathers optional Maya related data for Deadline
    """

    order = pyblish.api.ExtractorOrder
    hosts = ['maya']
    families = ['deadline']
    label = 'Layer to Deadline'

    def process(self, instance):

        # getting deadline data
        job_data = {}
        plugin_data = {}
        if instance.has_data('deadlineData'):
            job_data = instance.data('deadlineData')['job'].copy()
            plugin_data = instance.data['deadlineData']['plugin'].copy()
        else:
            instance.data['deadlineData'] = {}

        current_file = instance.context.data('currentFile')
        directory, filename = os.path.split(str(current_file))

        version = pymel.versions.fullName()
        build = pymel.versions.bitness()

        if 'ass' in instance.data['families']:
            job_data['Plugin'] = 'Arnold'
            job_data['group'] = 'arnold'
            job_data['LimitGroups'] = 'arnold'
            plugin_data['InputFile'] = instance.data['publishFile']
            plugin_data['LocalRendering'] = 'False'
            plugin_data['PluginFolder1'] = ''
            plugin_data['PluginFolder2'] = ''
            plugin_data['PluginFolder3'] = ''
            plugin_data['Version'] = 'Release'
            plugin_data['CommandLineOptions'] = ''
            plugin_data['Verbose'] = '4'
        else:
            job_data['Plugin'] = 'MayaBatch'
            job_data['LimitGroups'] = plugin_data['Renderer']
            job_data['Group'] = 'maya_' + abs(version).replace('.', '_')
            plugin_data['scene'] = instance.context.data['publishFile']
            plugin_data['ProjectPath'] = instance.data['projectPath']
            plugin_data['Version'] = version
            plugin_data['Build'] = build
            plugin_data['UsingRenderLayers'] = '1'

        job_data['Name'] = filename + " - " + instance.name
        job_data['UserName'] = instance.context.data['user']
        job_data['Pool'] = 'cg'
        job_data['Frames'] = instance.data['frames']
        job_data['OutputFilename0'] = instance.data['outputFilename']


        instance.data['deadlineData']['job'] = job_data
        instance.data['deadlineData']['plugin'] = plugin_data
