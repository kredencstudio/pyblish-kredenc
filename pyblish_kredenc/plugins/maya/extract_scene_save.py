import maya
import pyblish.api
import maya.app.renderSetup.model.renderSetup as renderSetup


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
        self.log.info('saving scene')
        maya.cmds.file(s=True)
