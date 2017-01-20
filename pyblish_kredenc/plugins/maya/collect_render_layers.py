import pyblish.api
import pymel.core as pm


@pyblish.api.log
class CollectRenderLayers(pyblish.api.ContextPlugin):
    """Collect Maya's scene units."""

    order = pyblish.api.CollectorOrder
    hosts = ["maya"]
    label = 'Render Layers'

    def process(self, context):

        drg = pm.PyNode('defaultRenderGlobals')

        projectPath = str(pm.system.Workspace.getPath().expand())


        for layer in pm.ls(type='renderLayer'):

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
            # try:
            #     pm.editRenderLayerGlobals(currentRenderLayer=legacyLayer)
            # except:
            #     continue

            # getting frames
            start_frame = str(int(drg.startFrame.get()))
            end_frame = str(int(drg.endFrame.get()))
            by_frame = int(drg.byFrameStep.get())
            frames = '{}-{}x{}'.format(start_frame, end_frame, by_frame)

            # Get the frame padding from render settings
            padding = drg.extensionPadding.get()
            padString = '#' * padding
            # start_frame_padded = start_frame.zfill(padding)
            renderPath = pm.renderSettings(fp=True, cts='RenderPass=beauty RenderLayer={}'.format(layer_name), gin=padString, lut=True)[0]
            # first_frame_path = pm.renderSettings(fp=True, gin=start_frame_padded, lyr=layer.name())[0]
            # renderPath = renderPath.replace((layer_name.split('_')[1]), (layer_name))
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
