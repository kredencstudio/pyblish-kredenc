import nuke
import pyblish.api


class ExtractSceneSave(pyblish.api.Extractor):
    """
    """
    hosts = ['nuke']
    order = pyblish.api.Extractor.order - 0.45
    families = ['scene']
    label = 'Scene Save'

    def process(self, instance):

        self.log.info('saving scene')
        nuke.scriptSave()
