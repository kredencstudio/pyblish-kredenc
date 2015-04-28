import nuke
import pyblish.api
import os


@pyblish.api.log
class SelectWorkfile(pyblish.api.Selector):
    """Selects all write nodes"""

    hosts = ['nuke']
    version = (0, 1, 0)

    def process_context(self, context):

        current_file = nuke.root().name()

        # Maya returns forward-slashes by default
        normalised = os.path.normpath(current_file)

        instance = context.create_instance(name='Current File')
        instance.set_data('family', value='workfile')
        instance.set_data("publish", False)
        instance.set_data("path", value=normalised)
        instance.add(normalised)
