import os
import pyblish.api
import pymel
import pymel.core as pm

@pyblish.api.log
class CollectRenderlayers(pyblish.api.Collector):
    """ Gathers all renderlayers
    TODO:
        - support frame range overrides
            - getting some odd returned values from the renderlayer adjustments
    """
    hosts = ['maya']

    def process(self, context):

        # getting output path
        render_globals = pm.PyNode('defaultRenderGlobals')
        start_frame = render_globals.startFrame.get()

        # getting job data
        job_data = {}
        if context.has_data('deadlineData'):
            job_data = context.data('deadlineData')['job'].copy()

        # storing plugin data
        plugin_data = {'UsingRenderLayers': 1}

        tmp = str(pm.system.Workspace.getPath().expand())
        plugin_data['ProjectPath'] = tmp

        plugin_data['Version'] = pymel.versions.fullName()
        plugin_data['Build'] = pymel.versions.bitness()

        drg = pm.PyNode('defaultRenderGlobals')

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
                    if layer.adjustments[count].plug.connections()[0] == drg:
                        attr = layer.adjustments[count].plug.connections(plugs=True)[0]
                        layer_data[attr.name(includeNode=False)] = layer.adjustments[count].value.get()
                data[layer.name()] = layer_data
            else:
                data[layer.name()] = {}

        # getting frames
        start_frame = int(render_globals.startFrame.get())
        end_frame = int(render_globals.endFrame.get())

        frames = '%s-%s' % (start_frame, end_frame)

        padding = render_globals.extensionPadding.get()
        padString = '#' * padding

        for layer in data:

            path = pm.renderSettings(fp=True, gin=padString, lyr=layer)[0]

            instance = context.create_instance(name=layer)
            instance.data['family'] = 'deadline.render'
            instance.data['families'] = ['deadline.render', 'render']

            instance.data['deadlineFrames'] = frames

            instance.data['data'] = data[layer]

            instance.data["publish"] = False

            # setting job data
            job_data = job_data.copy()

            safe_layer_name = layer.replace(':', '_')
            # outputFilename = path.format(layer=safe_layer_name,ext=ext)
            outputFile = path.format(layer=safe_layer_name)
            job_data['OutputFilename0'] = outputFile

            # setting plugin_data
            plugin_data = plugin_data.copy()
            plugin_data['RenderLayer'] = layer

            try:
                plugin_data['Renderer'] = data[layer]['currentRenderer']
            except:
                plugin_data['Renderer'] = drg.currentRenderer.get()

            # setting job data
            deadline_data = {'job': job_data, 'plugin': plugin_data}
            instance.data['deadlineData'] = deadline_data
            self.log.info(deadline_data)

            # adding ftrack data to activate processing
            instance.data['ftrackComponents'] = {}
            instance.data['ftrackAssetType'] = 'render'
