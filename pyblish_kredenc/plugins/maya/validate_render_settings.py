import os

import pymel
import pyblish.api

from ftrack_kredenc import ft_maya, ft_utils
reload(ft_maya)

def get_path(context):

    ftrack_data = context.data('ftrackData')
    taskid = context.data('ftrackData')['Task']['id']

    if 'Asset_Build' not in ftrack_data.keys():
        templates = [
            'shot.render'
        ]
    else:
        templates = [
            'asset.render'
        ]

    root = context.data('ftrackData')['Project']['root']
    renderFolder = ft_utils.getPathsYaml(taskid,
                                             templateList=templates,
                                             root=root)
    renderFolder = renderFolder[0]

    return renderFolder.replace('\\', '/')

class RepairRenderSettings(pyblish.api.Action):
    label = "Repair"
    on = "failed"
    icon = "wrench"

    def process(self, context, plugin):

        render_globals = pymel.core.PyNode('defaultRenderGlobals')

        # repairing current render layer
        layer = pymel.core.PyNode('defaultRenderLayer')
        pymel.core.nodetypes.RenderLayer.setCurrent(layer)

        # repairing frame/animation ext
        render_globals.animation.set(1)
        render_globals.outFormatControl.set(0)
        render_globals.putFrameBeforeExt.set(1)
        render_globals.extensionPadding.set(4)
        render_globals.periodInExt.set(1)

        # repairing frame padding
        render_globals.extensionPadding.set(4)

        publish_file = os.path.splitext(os.path.basename(context.data['publishFile']))[0]

        # repairing file name prefix
        expected_prefix = '<RenderLayer>/<Version>/{}_<RenderLayer>_<RenderPass>'.format(publish_file)
        render_globals.imageFilePrefix.set(expected_prefix)

        # repairing renderpass naming
        render_globals.multiCamNamingMode.set(1)
        render_globals.bufferName.set('<RenderPass>')

        # repairing workspace path
        path = os.path.dirname(pymel.core.system.sceneName())
        pymel.core.system.Workspace.open(path)

        # repairing default lighting
        render_globals.enableDefaultLight.set(False)

        version = context.data['version']
        render_globals.renderVersion.set('v' + version)

        # repairing image path
        output = get_path(context)
        pymel.core.system.Workspace.fileRules['images'] = output
        pymel.core.system.Workspace.save()


class ValidateRenderSettings(pyblish.api.InstancePlugin):
    """ Validates settings """

    order = pyblish.api.ValidatorOrder
    families = ['render']
    optional = True
    label = 'Render Settings'

    actions = [RepairRenderSettings]

    def process(self, instance):

        # if instance.context.data['ftrackData']['Task']['type'].lower() not in ['lighting', 'lookdev']:
        #     return

        if instance.context.has_data('renderOutputChecked'):
            return
        else:
            instance.context.set_data('renderOutputChecked', value=True)

        render_globals = pymel.core.PyNode('defaultRenderGlobals')

        fails = []

        # validate frame/animation ext
        msg = 'Frame/Animation ext is incorrect. Expected: "name.#.ext".'
        if (render_globals.animation.get() != 1 or
                render_globals.outFormatControl.get() != 0 or
                render_globals.putFrameBeforeExt.get() != 1 or
                render_globals.extensionPadding.get() != 4 or
                render_globals.periodInExt.get() != 1):
            fails.append(msg)

        # validate frame padding
        msg = 'Frame padding is incorrect. Expected: 4'
        if not render_globals.extensionPadding.get() == 4:
            fails.append(msg)

        # validate file name prefix
        msg = 'File name prefix is incorrect.'
        prefix = render_globals.imageFilePrefix.get()
        publish_file = os.path.splitext(os.path.basename(instance.context.data['publishFile']))[0]

        # repairing file name prefix
        expected_prefix = '<RenderLayer>/<Version>/{}_<RenderLayer>_<RenderPass>'.format(publish_file)
        if not prefix == expected_prefix:
            fails.append(msg)

        # # validate renderpass naming
        # msg = 'Renderpass naming is incorrect:'
        # msg += '\n\n"Frame Buffer Naming": "Custom"'
        # msg += '\n\n"Custom Naming String": "<RenderPass>"'
        # data = instance.data('data')
        # if 'multiCamNamingMode' in data:
        #     if (int(data['multiCamNamingMode']) != 1 or
        #             render_globals.bufferName.get() != '<RenderPass>'):
        #         fails.append(msg)

        # validate default lighting off
        msg = 'Default lighting is enabled.'
        if render_globals.enableDefaultLight.get():
            fails.append(msg)

        # ftrack dependent validation
        if not instance.context.has_data('ftrackData'):
            return

        # validate image path
        expected_output = get_path(instance.context)
        output = str(pymel.core.system.Workspace.fileRules['images'])
        msg = 'Project Images directory is incorrect.'
        msg += ' Expected: %s' % expected_output
        if not output == expected_output:
            fails.append(msg)

        version = instance.context.data['version']
        version_label = render_globals.renderVersion.get()
        msg = 'Version Label is incorrect.'
        msg += ' Expected: v{}'.format(version)
        if not version_label == ('v' + version):
            fails.append(msg)

        if len(fails) > 0:
            for fail in fails:
                self.log.error(fail)

        if len(fails)!=0:
            raise ValueError('Some things need to be fixed')
        assert len(fails) == 0, 'Some things need to be fixed/'
