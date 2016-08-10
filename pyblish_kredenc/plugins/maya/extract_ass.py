import pymel.core as pm
import pyblish.api
import pyblish_kredenc.utils as pyblish_utils
reload(pyblish_utils)
import pyblish_kredenc.actions as act
reload(act)


class ExtractAssLocal(pyblish.api.InstancePlugin):
    """Extracts arnold archive file.
    """
    order = pyblish.api.ExtractorOrder + 0.1
    families = ['arnold']
    optional = True
    label = '.ASS export Local'

    actions = [act.folders.OpenOutputFolder, act.folders.OpenOutputFile]

    def process(self, instance):

        instance.data['families'].append('ass.local')
        self.log.debug(instance.data)

        outputPath = instance.data['outputPath_ass']
        start_frame = instance.data['startFrame']
        end_frame = instance.data['endFrame']
        by_frame = instance.data['byFrame']

        options = '-startFrame {} '.format(start_frame)
        options += '-endFrame {} '.format(end_frame)
        options += '-frameStep {} '.format(by_frame)
        options += '-mask 255 \
                    -lightLinks 1 \
                    -forceTranslateShadingEngines \
                    -shadowLinks 2 \
                    -binary'

        self.log.info('Switching render layer to {}'.format(instance.name))
        pm.editRenderLayerGlobals(currentRenderLayer=instance.name)

        pm.exportAll(outputPath, f=1, typ="ASS Export", options=options)
