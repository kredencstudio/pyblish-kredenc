import os
import getpass
import tempfile
import pyblish.api

import nuke
import nukescripts



@pyblish.api.log
class ExtractDeadlineData(pyblish.api.Extractor):
    """Prepares All Deadline data"""

    families = ['writeNode', 'prerenders']
    hosts = ['nuke']
    version = (0, 1, 0)

    def process_instance(self, instance):

        node = instance[0]
        name = 'Submit "%s" to Deadline' % node.name()

        [job_path, plugin_path, scene_file] = [None, None, None]

        if instance.context.has_data('published_scene_file'):
            scene_file = instance.context.data('published_scene_file')
        else:
            scene_file = nuke.root().name()

        try:
            [job_path, plugin_path] = self.CreateFtrackJob(node, scene_file)
        except:
            [job_path, plugin_path] = self.CreateDeadlineJob(node, scene_file)

        instance.set_data('job_path', value=job_path)
        instance.set_data('plugin_path', value=plugin_path)
        instance.set_data('scene_file', value=scene_file)

    def CreateDeadlineJob(self, write_node, scene_file):

        # generating job file
        name = os.path.basename(nuke.root().name())
        username = getpass.getuser()
        start_frame = int(nuke.root()['first_frame'].getValue())
        end_frame = int(nuke.root()['last_frame'].getValue())

        output_path = write_node['file'].getValue()
        output_dir = os.path.dirname(output_path)
        output_file = os.path.basename(output_path).replace('%04d', '####')

        data = 'Name=%s\n' % name
        data += 'UserName=%s\n' % username
        data += 'Frames=%s-%s\n' % (start_frame, end_frame)
        data += 'ChunkSize=10\n'
        data += 'Group=nuke_90v4\n'
        data += 'Pool=medium\n'
        data += 'LimitGroups=nuke\n'
        data += 'OutputDirectory0=%s\n' % output_dir
        data += 'OutputFilename0=%s\n' % output_file
        data += 'Plugin=Nuke\n'

        name = '%s_job.txt' % write_node.name()
        job_path = os.path.join(tempfile.gettempdir(), name)
        job_file = open(job_path, 'w')
        job_file.write(data)
        job_file.close()

        # generating plugin file
        nukex = nuke.env['nukex']

        data = 'SceneFile=%s\n' % scene_file
        data += 'Version=9.0\n'
        data += 'WriteNode=%s\n' % write_node.name()
        data += 'Threads=0\n'
        data += 'RamUse=0\n'
        data += 'BatchMode=False\n'
        data += 'BatchModeIsMovie=False\n'
        data += 'NukeX=%s\n' % nukex
        data += 'UseGpu=False\n'
        data += 'ProxyMode=False\n'
        data += 'EnforceRenderOrder=False\n'
        data += 'ContinueOnError=False\n'
        data += 'PerformanceProfiler=False\n'
        data += 'PerformanceProfilerDir=\n'
        data += 'Views=\n'
        data += 'StackSize=0\n'

        name = '%s_plugin.txt' % write_node.name()
        plugin_path = os.path.join(tempfile.gettempdir(), name)
        plugin_file = open(plugin_path, 'w')
        plugin_file.write(data)
        plugin_file.close()

        return [job_path, plugin_path]

    def CreateFtrackJob(self, write_node, scene_file):

        import ftrack

        # generating job file
        name = os.path.basename(nuke.root().name())
        username = getpass.getuser()
        start_frame = int(nuke.root()['first_frame'].getValue())
        end_frame = int(nuke.root()['last_frame'].getValue())

        output_path = write_node['file'].getValue()
        output_dir = os.path.dirname(output_path)
        output_file = os.path.basename(output_path).replace('%04d', '####')
        height = nuke.root().format().height()
        width = nuke.root().format().width()

        component_name = write_node['fcompname'].getValue()

        task_id = os.environ['FTRACK_TASKID']
        task = ftrack.Task(id=os.environ['FTRACK_TASKID'])

        project_id = task.getProject().getId()

        asset_name = None
        asset_id = None
        for asset in task.getAssets():
            if asset.getType().getShort() == 'comp':
                asset_name = asset.getName()
                asset_id = asset.getId()
            else:
                asset_name = 'comp'

        version_number = int(nukescripts.version_get(output_path, 'v')[1])

        template = r"K:\.core\repos\DeadlineRepository7\custom\draft\encode_to_mov_h264_540p.py"

        data = 'Name=%s\n' % name
        data += 'UserName=%s\n' % username
        data += 'Frames=%s-%s\n' % (start_frame, end_frame)
        data += 'ChunkSize=10\n'
        data += 'Group=nuke\n'
        data += 'Pool=comp\n'
        data += 'LimitGroups=\n'
        data += 'OutputDirectory0=%s\n' % output_dir
        data += 'OutputFilename0=%s\n' % output_file
        data += 'Plugin=Nuke\n'
        # data += 'ExtraInfo0=%s\n' % task_name
        # data += 'ExtraInfo1=%s\n' % project_name
        # data += 'ExtraInfo2=%s\n' % asset_name
        # data += 'ExtraInfo3=%s\n' % version_number
        # data += 'ExtraInfo5=%s\n' % username

        data += 'ExtraInfoKeyValue0=DraftTemplate=%s\n' % template
        data += 'ExtraInfoKeyValue1=DraftExtraArgs=\n'
        data += 'ExtraInfoKeyValue2=DraftFrameHeight=%s\n' % height
        data += 'ExtraInfoKeyValue3=DraftFrameWidth=%s\n' % width
        data += 'ExtraInfoKeyValue4=DraftVersion=\n'
        data += 'ExtraInfoKeyValue5=DraftUploadToFtrack=True\n'
        data += 'ExtraInfoKeyValue6=DraftUsername=\n'
        data += 'ExtraInfoKeyValue7=DraftEntity=\n'


        data += 'ExtraInfoKeyValue8=FT_TaskId=%s\n' % task_id
        data += 'ExtraInfoKeyValue9=FT_ProjectId=%s\n' % project_id

        data += 'ExtraInfoKeyValue10=FT_AssetName=%s\n' % asset_name
        data += 'ExtraInfoKeyValue11=FT_AssetId=%s\n' % asset_id

        data += 'ExtraInfoKeyValue12=FT_VersionNumber=%s\n' % version_number
        data += 'ExtraInfoKeyValue13=FT_VersionId=\n'

        data += 'ExtraInfoKeyValue14=FT_ComponentName=%s\n' % component_name

        data += 'ExtraInfoKeyValue15=FT_Username=%s\n' % username
        data += 'ExtraInfoKeyValue16=FT_Description=\n'



        name = '%s_job.txt' % write_node.name()
        job_path = os.path.join(tempfile.gettempdir(), name)
        job_file = open(job_path, 'w')
        job_file.write(data)
        job_file.close()

        # generating plugin file
        nukex = nuke.env['nukex']

        data = 'SceneFile=%s\n' % scene_file
        data += 'Version=9.0\n'
        data += 'WriteNode=%s\n' % write_node.name()
        data += 'Threads=0\n'
        data += 'RamUse=0\n'
        data += 'BatchMode=False\n'
        data += 'BatchModeIsMovie=False\n'
        data += 'NukeX=%s\n' % nukex
        data += 'UseGpu=False\n'
        data += 'ProxyMode=False\n'
        data += 'EnforceRenderOrder=False\n'
        data += 'ContinueOnError=False\n'
        data += 'PerformanceProfiler=False\n'
        data += 'PerformanceProfilerDir=\n'
        data += 'Views=\n'
        data += 'StackSize=0\n'

        name = '%s_plugin.txt' % write_node.name()
        plugin_path = os.path.join(tempfile.gettempdir(), name)
        plugin_file = open(plugin_path, 'w')
        plugin_file.write(data)
        plugin_file.close()

        return [job_path, plugin_path]
