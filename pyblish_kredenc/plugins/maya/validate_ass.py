import pymel.core as pm
import pyblish.api


class ValidateAss(pyblish.api.InstancePlugin):
    """Extracts arnold archive file.
    """
    order = pyblish.api.ValidatorOrder
    families = ['ass.render']
    optional = True

    def process(self, instance):

        pm.editRenderLayerGlobals(currentRenderLayer=instance.name)
        self.log.info('Switching render layer to {}'.format(instance.name))
