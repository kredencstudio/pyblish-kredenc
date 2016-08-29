import pyblish.api


class AddFtrackData(pyblish.api.InstancePlugin):
    """ Add ftrack components data"""

    order = pyblish.api.ExtractorOrder
    families = ['render', 'mov.*']

    def process(self, instance):

        files = instance.data["files"]
        self.log.info("Integrating files: " + str(files))

        instance.data['ftrackComponents'] = {}

        families = instance.data['families']

        upload = False
        if 'render' in families:
            component_name = 'main'
        elif 'mov.*' in families:
            component_name = 'review'
            upload = True
        else:
            component_name = 'dealine'

        for filename in files:
            instance.data['ftrackComponents'][component_name] = {
                'path': filename,
                'reviewable': upload
                }
