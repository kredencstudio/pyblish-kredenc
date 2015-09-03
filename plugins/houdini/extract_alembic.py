import pyblish.api
import shutil
import hou
import os


@pyblish.api.log
class ExtractAlembic(pyblish.api.Extractor):
    """Creates preview movie from a Flipbook bode"""

    families = ['cache']
    hosts = ['houdini']
    version = (0, 1, 0)
    label = 'Alembic Cache'

    def process(self, instance, context):
        # extracting camera

        out = hou.node('/out')
        currentFile = context.data('currentFile')

        root, ext = os.path.splitext(currentFile)

        filepath = '{0}_{1}.abc'.format(root, instance.data('name'))

        abc_rop = instance[0]
        abc_rop.setParms({'trange': 1,
                          'filename': filepath,
                          'partition_mode': 4,
                          'collapse': 1,
                          })

        instance.set_data('outputPath', value=filepath)
        abc_rop.render()
