import pyblish.api
import pymel.core as pm
import maya.app.renderSetup.model.renderSetup as renderSetup

@pyblish.api.log
class CollectRenderLayers(pyblish.api.ContextPlugin):
    """Collect Maya render layers."""

    order = pyblish.api.CollectorOrder
    hosts = ["maya"]
    label = 'Render Layers'

    def process(self, context):

        drg = pm.PyNode('defaultRenderGlobals')

        projectPath = str(pm.system.Workspace.getPath().expand())
        renderSetup.initialize()
        rs = renderSetup.instance()
        layers = rs.getRenderLayers()

        for layer in layers:

            # legacyLayer = layer
            # legacyLayer = pm.PyNode(layer.legacyRenderLayer.get())

            layer_name = layer.name()

            # skipping defaultRenderLayers
            if 'defaultRenderLayer' in layer_name:
                continue

            # skipping non renderable layers
            # if not legacyLayer.renderable.get():
            #     continue


            # Switch to renderlayer
            self.log.info('Switching render layer to {}'.format(layer_name))
            rs.switchToLayer(layer)
            self.log.info('Switched render layer to {}'.format(layer_name))

            renderpass = "beauty"
            if context.data.get('ftrackData'):
                if context.data['ftrackData']['Project']['code'] == 'hbt':
                    renderpass = 'diffuse_color'

            # getting frames
            start_frame = str(int(drg.startFrame.get()))
            end_frame = str(int(drg.endFrame.get()))
            by_frame = int(drg.byFrameStep.get())
            frames = '{}-{}x{}'.format(start_frame, end_frame, by_frame)

            layer_name_clean = layer_name.replace('rs_', '')

            # Get the frame padding from render settings
            padding = drg.extensionPadding.get()
            padString = '#' * padding
            # start_frame_padded = start_frame.zfill(padding)
            renderPath = pm.renderSettings(fp=True, cts='RenderPass={} RenderLayer={}'.format(renderpass, layer_name), gin=padString, lut=True)[0]
            # first_frame_path = pm.renderSettings(fp=True, gin=start_frame_padded, lyr=layer.name())[0]
            renderPath = renderPath.replace(layer_name, layer_name_clean)
            self.log.debug('render files: {}'.format(renderPath))
            self.log.debug('frames: {}'.format(frames))

            # create renderlayer instance
            instance = context.create_instance(layer_name, family='render')

            # set basic render layer familier
            instance.data['families'] = ['deadline', 'render']

            # add ass family if we're using arnold
            renderer = drg.currentRenderer.get()
            instance.data['families'].append(renderer)
            self.log.debug('families: {}'.format(instance.data['families']))

            # populate instance with data
            instance.data['startFrame'] = start_frame
            instance.data['endFrame'] = end_frame
            instance.data['byFrame'] = by_frame
            instance.data['frames'] = frames
            instance.data['projectPath'] = projectPath
            instance.data['outputFilename'] = renderPath
            instance.data['padding'] = padding
            instance.data['renderer'] = renderer
            # instance.data['outputPath_ass'] = outputPath
            # instance.data['inputPath'] = inputPath

            instance.data["publish"] = True

            components = {}
            compname = None

            if 'main' in layer_name:
                compname = 'main'
            else:
                compname = layer_name
            #
            if compname:
                components[compname] = {}

            # adding ftrack data to activate processing
            instance.data['ftrackComponents'] = components

            self.log.debug('collected: {}'.format(layer_name))

        master_layer = rs.getDefaultRenderLayer()
        rs.switchToLayer(master_layer)
