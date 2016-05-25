import pyblish.api
import pymel.core as pm
import os


@pyblish.api.log
class CollectAssExport(pyblish.api.ContextPlugin):
    """Collect Maya's scene units."""

    order = pyblish.api.CollectorOrder
    hosts = ["maya"]

    def process(self, context):

        drg = pm.PyNode('defaultRenderGlobals')

        renderer = drg.currentRenderer.get()

        # only continue if we're using arnold
        if renderer != 'arnold':
            return

        # getting job data
        job_data = {}
        if context.has_data('deadlineData'):
            job_data = context.data('deadlineData')['job'].copy()


        plugin_data = {}
        if context.has_data('deadlineData'):
            plugin_data = context.data('deadlineData')['plugin'].copy()

        # getting frames
        start_frame = str(int(drg.startFrame.get()))
        end_frame = str(int(drg.endFrame.get()))

        frames = '%s-%s' % (start_frame, end_frame)

        for layer in pm.ls(type='renderLayer'):

            # skipping non renderable layers
            if not layer.renderable.get():
                continue

            # skipping defaultRenderLayers
            if 'defaultRenderLayer' in layer.name():
                continue

            padding = drg.extensionPadding.get()
            padString = '#' * padding
            numberPadded = start_frame.zfill(padding)
            renderPath = pm.renderSettings(fp=True, gin=padString, lyr=layer.name())[0]
            first_frame_path = pm.renderSettings(fp=True, gin=numberPadded, lyr=layer.name())[0]
            self.log.info(renderPath)

            path, ext = os.path.splitext(first_frame_path)
            folder, filename = os.path.split(path)
            outputPath = os.path.join(folder, 'ass', filename + '.ass')
            self.log.info(outputPath)

            instance = context.create_instance(layer.name(), family='ass.render')
            instance.data['families'] = ['ass.render', 'deadline.render']
            instance.data['startFrame'] = start_frame
            instance.data['endFrame'] = end_frame
            instance.data['outputPath_ass'] = outputPath

            instance.data["publish"] = False

            job_data['OutputFilename0'] = renderPath
            job_data['Plugin'] = 'Arnold'
            job_data['Frames'] = frames
            plugin_data['InputFile'] = outputPath

            # setting job data
            deadline_data = {'job': job_data, 'plugin': plugin_data}
            instance.data['deadlineData'] = deadline_data
            self.log.info(deadline_data)

            # adding ftrack data to activate processing
            instance.data['ftrackComponents'] = {}
            instance.data['ftrackAssetType'] = 'render'
