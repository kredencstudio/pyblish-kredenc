import hou
import pyblish.api

@pyblish.api.log
class SelectMantraNodes(pyblish.api.Selector):
    """Selects all cam nodes"""

    hosts = ['houdini']
    version = (0, 1, 0)

    def process(self, context):

        node_type = hou.nodeType('Object/cam')
        cam_nodes = node_type.instances()

        for node in list(cam_nodes):

            if 'ipr' not in node.name():
                instance = context.create_instance(name=node.name())
                instance.set_data('family', value='camera')
                instance.set_data('path', value=node.path())
                instance.add(node)
