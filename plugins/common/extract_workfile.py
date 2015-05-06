import pyblish.api
import shutil


@pyblish.api.log
class PublishWorkfile(pyblish.api.Extractor):
    """Publishes current workfile to a _Publish location, next to current working directory"""

    families = ['workFile']
    hosts = ['*']
    version = (0, 1, 0)
    optional = True

    def process_instance(self, instance):
        # submitting job
        sourcePath = instance.data('path')
        new_workfile = instance.context.data('new_workfile')
        publishPath = instance.context.data('published_scene_file')
        shutil.copy(sourcePath, publishPath)