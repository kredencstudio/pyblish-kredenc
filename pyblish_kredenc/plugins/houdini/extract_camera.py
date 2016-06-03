import pyblish.api
import hou
import os


@pyblish.api.log
class ExtractCamera(pyblish.api.Extractor):
    """Creates preview movie from a Flipbook bode"""

    families = ['camera']
    hosts = ['houdini']
    version = (0, 1, 0)
    label = 'ABC camera'

    def process(self, instance, context):
        # extracting camera

        out = hou.node('/out')
        currentFile = context.data('currentFile')

        root, ext = os.path.splitext(currentFile)

        filepath = '{0}_cam.abc'.format(root)

        abc_rop = out.createNode("alembic")
        abc_rop.setParms({'trange': 1,
                          'filename': filepath,
                          'objects': instance.data('path'),
                          'partition_mode': 4,
                          'collapse': 1,
                          })

        instance.set_data('outputPath', value=filepath)
        abc_rop.render()
        abc_rop.destroy()
