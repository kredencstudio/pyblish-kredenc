import maya
import pyblish.api
import maya.app.renderSetup.model.renderSetup as renderSetup

import pymel.core as pm


class ExtractSceneSave(pyblish.api.Extractor):
    """
    """
    hosts = ['maya']
    order = pyblish.api.Extractor.order - 0.45
    families = ['scene']
    label = 'Scene Save'

    def process(self, instance):

        rs = renderSetup.instance()
        master_layer = rs.getDefaultRenderLayer()
        rs.switchToLayer(master_layer)

        self.log.info("SCENE SAVE")

        if instance.context.data.get('ftrackData'):
            if instance.context.data['ftrackData']['Project']['code'] == 'hbt':
                self.log.info("Switching texures to PROXY")
                import hbt_switch_tex as hbtSw
                reload(hbtSw)

                nhbtData=hbtSw.switchTexture()

                nhbtData.option = 2
                nhbtData.highest = False
                nhbtData.limit = 1600
                nhbtData.validatorCheck()
                nhbtData.fast = False

                nhbtData.all = True
                nhbtData.switch()
                pm.refresh(f = True)

                self.log.info("Switched to PROXY before save")

        self.log.info('saving scene')
        maya.cmds.file(s=True)
