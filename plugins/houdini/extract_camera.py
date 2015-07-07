import pyblish.api
import shutil
import hou
import _alembic_hom_extensions as abc


@pyblish.api.log
class ExtractCamera(pyblish.api.Extractor):
    """Creates preview movie from a Flipbook bode"""

    families = ['camera']
    hosts = ['houdini']
    version = (0, 1, 0)
    label = 'ABC camera'

    def process(self, instance):
        # extracting camera
        self.log.info('Extracting cameras from houdini is not supported yet.\
                      I\'m doing my best to fix this!')
