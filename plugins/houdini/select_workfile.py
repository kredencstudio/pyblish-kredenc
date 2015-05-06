import pyblish.api
import os

import hou

@pyblish.api.log
class SelectWorkfile(pyblish.api.Selector):
    """Selects current workfile"""

    hosts = ['*']
    version = (0, 1, 0)

    def process_context(self, context):

        current_file = hou.hipFile.path()

        # Maya returns forward-slashes by default
        normalised = os.path.normpath(current_file)

        directory, filename = os.path.split(normalised)

        instance = context.create_instance(name=filename)
        instance.set_data('family', value='workFile')
        # instance.set_data("publish", False)
        instance.set_data("path", value=normalised)
        instance.add(normalised)
