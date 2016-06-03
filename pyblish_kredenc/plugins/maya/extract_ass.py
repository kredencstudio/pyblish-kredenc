import pymel.core as pm
import pyblish.api


class ExtractAss(pyblish.api.InstancePlugin):
    """Extracts arnold archive file.
    """
    order = pyblish.api.ExtractorOrder - 0.1
    families = ['ass.render']
    optional = True

    def process(self, instance):


        outputPath = instance.data['outputPath_ass']
        start_frame = instance.data['startFrame']
        end_frame = instance.data['endFrame']

        options = '-startFrame {} '.format(start_frame)
        options += '-endFrame {} '.format(end_frame)
        options += '-mask 255 \
                    -lightLinks 1 \
                    -forceTranslateShadingEngines \
                    -frameStep 1.0 \
                    -shadowLinks 2 \
                    -binary'


        self.log.info('Switching render layer to {}'.format(instance.name))
        pm.editRenderLayerGlobals(currentRenderLayer=instance.name)


        pm.exportAll(outputPath, f=1, typ="ASS Export", options=options)
