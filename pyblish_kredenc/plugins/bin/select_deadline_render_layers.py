import os
import traceback

import pyblish.api
import pymel
import maya


@pyblish.api.log
class SelectDeadlineRenderlayers(pyblish.api.Selector):
    """ Gathers all renderlayers
    """

    hosts = ['maya']
    version = (0, 1, 0)
    name = 'Select Renderlayers'

    def process(self, context):

        # getting output path
        render_globals = pymel.core.PyNode('defaultRenderGlobals')
        start_frame = render_globals.startFrame.get()

        # getting job data
        job_data = {}
        if context.has_data('deadlineJobData'):
            job_data = context.data('deadlineJobData').copy()

        # storing plugin data
        plugin_data = {'UsingRenderLayers': 1}

        tmp = str(pymel.core.system.Workspace.getPath().expand())
        plugin_data['ProjectPath'] = tmp

        plugin_data['Version'] = pymel.versions.flavor()
        plugin_data['Build'] = pymel.versions.bitness()

        drg = pymel.core.PyNode('defaultRenderGlobals')

        # arnold specifics
        if drg.currentRenderer.get() == 'arnold':
            plugin_data['Animation'] = 1

        # storing modified state
        modified = maya.cmds.file(q=True, mf=True)

        # turn display off
        pymel.core.general.select(clear=True)
        panel = pymel.core.getPanel(withFocus=True)
        pymel.core.general.isolateSelect(panel, state=1)

        try:
            for layer in pymel.core.ls(type='renderLayer'):

                if layer.renderable.get() and \
                ':defaultRenderLayer' not in layer.name():

                    layer.setCurrent()

                    instance = context.create_instance(name=layer.name())
                    instance.set_data('family', value='deadline.render')

                    # getting layer name
                    if layer.name() == 'defaultRenderLayer':
                        layer_name = 'masterLayer'
                    else:
                        layer_name = layer.name()

                    # setting plugin_data
                    plugin_data = plugin_data.copy()
                    plugin_data['RenderLayer'] = layer_name
                    plugin_data['Renderer'] = drg.currentRenderer.get()

                    instance.set_data('deadlinePluginData', value=plugin_data)

                    # setting job data
                    job_data = job_data.copy()

                    start_frame = int(render_globals.startFrame.get())
                    end_frame = int(render_globals.endFrame.get())
                    frames = '%s-%s' % (start_frame, end_frame)
                    instance.set_data('deadlineFrames', value=frames)

                    paths = [str(pymel.core.system.Workspace.getPath().expand())]
                    try:
                        paths.append(str(pymel.core.system.Workspace.fileRules['images']))
                    except:
                        pass

                    output_path = os.path.join(*paths)
                    tmp = pymel.core.rendering.renderSettings(firstImageName=True)[0]
                    paths.append(str(tmp))

                    path = os.path.join(*paths)

                    padding = render_globals.extensionPadding.get()
                    firstFrame = int(render_globals.startFrame.get())
                    stringFrame = str(firstFrame).zfill(padding)
                    if stringFrame in os.path.basename(path):
                        tmp = '#' * padding
                        basename = os.path.basename(path).replace(stringFrame, tmp)
                        dirname = os.path.dirname(path)
                        path = os.path.join(dirname, basename)

                    if layer.name() == 'defaultRenderLayer':
                        path = path.replace('defaultRenderLayer', layer_name)

                    job_data['OutputFilename0'] = path

                    instance.set_data('deadlineJobData', value=job_data)

                    # adding ftrack data to activate processing
                    instance.set_data('ftrackComponents', value={})
                    instance.set_data('ftrackAssetType', value='img')
        except:
            self.log.info(traceback.format_exc)

        pymel.core.general.isolateSelect(panel, state=0)

        if not modified:
            maya.cmds.file(s=True)
