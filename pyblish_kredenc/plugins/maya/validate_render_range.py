import os

import pymel
import pymel.core as pm
import pyblish.api

from ftrack_kredenc import ft_maya
reload(ft_maya)
import ftrack_api
reload(ftrack_api)


def checkFtrackRange():
    shotId = os.getenv('FTRACK_SHOTID')

    session = ftrack_api.Session()
    shot = session.query('Shot where id is {}'.format(shotId)).one()

    handles = int(shot['custom_attributes']['handles'])
    sf = int(shot['custom_attributes']['fstart'])
    ef = int(shot['custom_attributes']['fend'])

    return[sf,ef,handles]


class RepairRenderRange(pyblish.api.Action):
    label = "Repair"
    on = "failed"
    icon = "wrench"

    def process(self, context, plugin):
        sf, ef , handle = checkFtrackRange()

        render_globals = pm.PyNode('defaultRenderGlobals')

        render_globals.startFrame.set( sf - handle)
        render_globals.endFrame.set(ef + handle)



class ValidateRenderRange(pyblish.api.InstancePlugin):
    """ Validates range """

    order = pyblish.api.ValidatorOrder
    families = ['render']
    optional = True
    label = 'Render Range'

    actions = [RepairRenderRange]

    def process(self, instance):

        if instance.context.has_data('renderRangeChecked'):
            return
        else:
            instance.context.set_data('renderRangeChecked', value=True)

        fails = []

        #try:
        sf, ef , handle = checkFtrackRange()

        render_globals = pm.PyNode('defaultRenderGlobals')

        start_frame = int(render_globals.startFrame.get())
        end_frame = int(render_globals.endFrame.get())

        msg = 'Render frame range does not match Ftrack data'
        if ((sf - handle) != start_frame) or ((ef + handle) != end_frame):
            fails.append(msg)


        if len(fails) > 0:
            for fail in fails:
                self.log.error(fail)

        if len(fails)!=0:
            raise ValueError('Some things need to be fixed')
        assert len(fails) == 0, 'Some things need to be fixed/'


        #except:
        #    self.log.info('render range check only supported on shots')
