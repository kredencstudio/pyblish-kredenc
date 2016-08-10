import pymel.core as pm
import pyblish.api
import pyblish_kredenc.utils as pyblish_utils
reload(pyblish_utils)
import pyblish_kredenc.actions as act
reload(act)


class ExtractAssFarm(pyblish.api.InstancePlugin):
    """Extracts arnold archive file.
    """
    order = pyblish.api.ExtractorOrder + 0.1
    families = ['arnold']
    optional = False
    label = '.ASS export to Deadline'
    active = False

    actions = [act.folders.OpenOutputFolder, act.folders.OpenOutputFile]

    def process(self, instance):

        instance.data['families'].append('ass.farm')
        self.log.debug(instance.data)

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

        instance.data['ass_options'] = options
