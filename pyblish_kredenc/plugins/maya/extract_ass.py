import pymel.core as pm
import pyblish.api
import pyblish_kredenc.utils as pyblish_utils
reload(pyblish_utils)
from pyblish_kredenc.actions import actions_os
import maya.app.renderSetup.model.renderSetup as renderSetup


import os

class ExtractAssLocal(pyblish.api.InstancePlugin):
    """Extracts arnold archive file.
    """
    order = pyblish.api.ExtractorOrder + 0.1
    families = ['arnold']
    optional = True
    label = '.ASS export'

    actions = [actions_os.OpenOutputFolder, actions_os.OpenOutputFile]


    def process(self, instance):
        self.log.info("????????UTILS FOR ASS EXPORT?????????")
        def forceOffAiAutoGen():
            fls = pm.ls(type = 'file')
            for f in fls:
                try:
                    pm.setAttr(f + '.aiAutoTx', 0)
                except:
                    pass

        def forceAnimLoad():
            fFrame = pm.playbackOptions(q = True, minTime = True)
            eFrame = pm.playbackOptions(q = True, maxTime = True)
            pm.currentTime(fFrame, e = True)
            pm.currentTime(eFrame, e = True)
            pm.currentTime(fFrame, e = True)
            pm.currentTime(eFrame, e = True)

        self.log.info("?????????????????????????????????????????")
        #if instance.context.data.get('ftrackData'):

        if instance.context.data('ftrackData')['Project']['code'] == 'hbt':
            self.log.info("Switching texures to High")
            import hbt_switch_tex as hbtSw
            reload(hbtSw)

            nhbtData=hbtSw.switchTexture()

            nhbtData.option = 0
            nhbtData.validatorCheck()

            for s in nhbtData.valid_shapes:
                try:
                    s.aiOpaque.set(0)
                except:
                    pass

            nhbtData.fast = True

            nhbtData.all = True
            nhbtData.switch()
            pm.refresh(f = True)

            self.log.info("switched to high resolution before ass extract")

        instance.data['families'].append('ass.local')
        self.log.debug(instance.data)

        outputPath = instance.data['outputPath_ass']
        outputFldr = os.path.dirname(outputPath)
        start_frame = instance.data['startFrame']
        end_frame = instance.data['endFrame']
        by_frame = instance.data['byFrame']

        options = '-startFrame {} '.format(start_frame)
        options += '-endFrame {} '.format(end_frame)
        options += '-frameStep {} '.format(by_frame)
        options += '-mask 2303 \
                    -lightLinks 1 \
                    -forceTranslateShadingEngines \
                    -shadowLinks 2\
                    -asciiAss\
                    '

        self.log.info('Switching render layer to {}'.format(instance.name))
        renderSetup.initialize()
        rs = renderSetup.instance()
        lyr = rs.getRenderLayer(instance.name)
        rs.switchToLayer(lyr)
        self.log.debug('Exporting ass')

        #this is maybe better export way
        pm.refresh()
        self.log.info("EXPORT ASS path: {}".format(outputPath))

        forceOffAiAutoGen()
        forceAnimLoad()

        arnoldOptions = None
        pm.arnoldExportAss(filename=outputPath, selected=False,
            sf=int(start_frame), ef=int(end_frame),
            frameStep=int(by_frame), asciiAss=True)
        if not os.path.isdir(outputFldr):
            pm.exportAll(outputPath, f=1, typ="ASS Export", options=options)

        self.log.debug('Export succesfull')
        master_layer = rs.getDefaultRenderLayer()
        rs.switchToLayer(master_layer)

        if instance.context.data.get('ftrackData'):
            if instance.context.data['ftrackData']['Project']['code'] == 'hbt':
                self.log.info("Switching texures to Proxy")
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

                self.log.info("switched to proxy resolution after ass extract")
