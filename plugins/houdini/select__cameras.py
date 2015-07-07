import hou
import pyblish.api

@pyblish.api.log
class SelectMantraNodes(pyblish.api.Selector):
    """Selects all cam nodes"""

    hosts = ['houdini']
    version = (0, 1, 0)

    def process(self, context):

        nodes = hou.node("/").allSubChildren()

        for node in list(nodes):

            if node.type().name() == 'cam' and node.name() != 'ipr_camera':
                instance = context.create_instance(name=node.name())
                instance.set_data('family', value='camera')
                instance.add(node)
