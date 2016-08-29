import pymel
import pyblish.api
import os
from maya import cmds


class RepairFR(pyblish.api.Action):
    label = "Repair"
    on = "failed"
    icon = "wrench"
    enabled = False

    def process(self, context):

        render_globals = pymel.core.PyNode('defaultRenderGlobals')

        sf_render = render_globals.startFrame.get()
        ef_render = render_globals.endFrame.get()

        sf_env = float(os.getenv('FS'))
        ef_env = float(os.getenv('FE'))

        sf_timeline = cmds.playbackOptions(minTime=True, q=True)
        ef_timeline = cmds.playbackOptions(maxTime=True, q=True)

        if not sf_env == ef_env:
            render_globals.startFrame.set(sf_env)
            render_globals.endFrame.set(sf_env)
        else:
            render_globals.startFrame.set(sf_timeline)
            render_globals.endFrame.set(ef_timeline)


@pyblish.api.log
class ValidateFrameRange(pyblish.api.Validator):
    """ Validates settings """
    order = pyblish.api.Validator.order
    hosts = ['maya']
    families = ['render']
    optional = True
    label = 'Frame Range'

    actions = [RepairFR]

    def process(self, instance):

        if instance.context.data['ftrackData']['Task']['type'] not in ['Lighting']:
            return


        render_globals = pymel.core.PyNode('defaultRenderGlobals')

        sf_render = render_globals.startFrame.get()
        ef_render = render_globals.endFrame.get()

        sf_env = float(os.getenv('FS'))
        ef_env = float(os.getenv('FE'))

        sf_timeline = cmds.playbackOptions(minTime=True, q=True)
        ef_timeline = cmds.playbackOptions(maxTime=True, q=True)

        msg = None

        if not sf_env == ef_env:
            if (sf_render != sf_env) or (ef_render != ef_env):
                msg = 'Start and end frames don\'t match this shot framerange'
        else:
            if (sf_render != sf_timeline) or (ef_render != ef_timeline):
                msg = 'Start and end frames don\'t match your framerange'

        assert not msg, msg
