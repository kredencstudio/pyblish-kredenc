import pyblish.api
import shutil

import nuke

@pyblish.api.log
class publishWorkfile(pyblish.api.Extractor):
    """Publishes current workfile to a _Publish location, next to current working directory"""

    order = pyblish.api.Extractor.order + 0.1
    families = ['workFile']
    hosts = ['nuke']
    version = (0, 1, 0)
    optional = True

    def process_instance(self, instance):
        # submitting job
        sourcePath = instance.data('path')
        new_workfile = instance.data('new_workfile')
        publishPath = instance.context.data('published_scene_file')

        shutil.copy(sourcePath, publishPath)
        nuke.scriptSaveAs(new_workfile)


