import pyblish.api


class AddFtrackData(pyblish.api.InstancePlugin):
    """ Add ftrack components data"""

    order = pyblish.api.ExtractorOrder
    families = ['render', 'mov.*']

    def process(self, instance):

        files = instance.data["files"]
        self.log.info("Integrating files: " + str(files))

        ftrack_components = instance.data.get('ftrackComponents')
        upload = False

        if ftrack_components:
            component_name = ftrack_components.keys()[0]
            upload = ftrack_components[component_name].get('reviewable')
        else:
            instance.data['ftrackComponents'] = {}
            component_name = 'deadline'

        families = instance.data['families']

        if 'render' in families:
            component_name = 'main'

        for filename in files:
            instance.data['ftrackComponents'][component_name] = {
                'path': filename,
                'reviewable': upload
                }

            self.log.info("Integrating Component: " + str(instance.data['ftrackComponents'][component_name]))
