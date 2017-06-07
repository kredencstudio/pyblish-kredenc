import pyblish.api
import os
import pymel

@pyblish.api.log
class ExtractDeadlineLayer(pyblish.api.InstancePlugin):
    """ Gathers optional Maya related data for Deadline
    """

    order = pyblish.api.ExtractorOrder + 0.3
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

        hostversion = pymel.versions.fullName()
        build = pymel.versions.bitness()


        if 'ass.farm' in instance.data['families']:
            self.log.info('ASS export on the farm are not yet supported')
        elif 'ass.local' in instance.data['families']:
            job_data['Plugin'] = 'Arnold'
            job_data['group'] = 'arnold'
            job_data['LimitGroups'] = instance.data['renderer']
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
            job_data['LimitGroups'] = instance.data['renderer']
            job_data['Group'] = 'maya_' + hostversion.replace('.', '_')
            plugin_data['SceneFile'] = instance.context.data['publishFile']
            plugin_data['ProjectPath'] = instance.data['projectPath']
            plugin_data['Version'] = hostversion
            plugin_data['Build'] = build
            plugin_data['Renderer'] = instance.data['renderer']
            plugin_data['UsingRenderLayers'] = '1'
            plugin_data['RenderLayer'] = instance.name

        job_data['Name'] = filename + " - " + instance.name
        job_data['UserName'] = instance.context.data['user']
        job_data['Pool'] = 'cg'
        job_data['Frames'] = instance.data['frames']
        job_data['OutputFilename0'] = instance.data['outputFilename']


        instance.data['deadlineData']['job'] = job_data
        instance.data['deadlineData']['plugin'] = plugin_data
