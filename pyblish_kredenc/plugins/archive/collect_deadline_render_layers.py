import pyblish.api
import pymel.core as pm


@pyblish.api.log
class CollectRenderlayers(pyblish.api.Collector):
    """ Gathers all renderlayers
    """
    hosts = ['maya']

    def process(self, context):

        # getting output path
        render_globals = pm.PyNode('defaultRenderGlobals')

        projectPath = str(pm.system.Workspace.getPath().expand())


        # getting render layers data
        data = {}
        for layer in pm.ls(type='renderLayer'):

            # skipping non renderable layers
            if not layer.renderable.get():
                continue

            # skipping defaultRenderLayers
            if 'defaultRenderLayer' in layer.name():
                continue

            layer_data = {}
            if layer.adjustments.get(multiIndices=True):
                for count in layer.adjustments.get(multiIndices=True):
                    if layer.adjustments[count].plug.connections()[0] == render_globals:
                        attr = layer.adjustments[count].plug.connections(plugs=True)[0]
                        layer_data[attr.name(includeNode=False)] = layer.adjustments[count].value.get()
                data[layer.name()] = layer_data
            else:
                data[layer.name()] = {}

        # getting frames
        start_frame = int(render_globals.startFrame.get())
        end_frame = int(render_globals.endFrame.get())
        by_frame = int(render_globals.byFrameStep.get())

        frames = '{}-{}x{}'.format(start_frame, end_frame, by_frame)

        padding = render_globals.extensionPadding.get()
        padString = '#' * padding

        for layer in data:

            path = pm.renderSettings(fp=True, gin=padString, lyr=layer)[0]

            #create instance

            instance = context.create_instance(name=layer)
            instance.data['startFrame'] = int(start_frame)
            instance.data['endFrame'] = int(end_frame)
            instance.data['byFrame'] = by_frame
            instance.data['family'] = 'render'
            instance.data['families'] = ['deadline', 'render']
            instance.data['data'] = data[layer]
            instance.data["publish"] = False
            instance.data['projectPath'] = projectPath

            # getting job data
            job_data = {}
            if context.has_data('deadlineData'):
                job_data = context.data('deadlineData')['job'].copy()

            # setting job data
            safe_layer_name = layer.replace(':', '_')
            outputFile = path.format(layer=safe_layer_name)
            job_data['OutputFilename0'] = outputFile
            job_data['Frames'] = frames

            # setting plugin_data
            plugin_data = {}

            plugin_data['RenderLayer'] = layer
            try:
                plugin_data['Renderer'] = data[layer]['currentRenderer']
            except:
                plugin_data['Renderer'] = render_globals.currentRenderer.get()

            # add deadline data
            deadline_data = {'job': job_data, 'plugin': plugin_data}
            instance.data['deadlineData'] = deadline_data

            # adding ftrack data to activate processing
            instance.data['ftrackComponents'] = {}
            instance.data['ftrackAssetType'] = 'render'
