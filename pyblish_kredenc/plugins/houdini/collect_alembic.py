import hou
import pyblish.api

@pyblish.api.log
class CollectAlembicRops(pyblish.api.Collector):
    """Selects all cam nodes"""

    hosts = ['houdini']
    version = (0, 1, 0)

    def process(self, context):

        node_type = hou.nodeType(hou.ropNodeTypeCategory(), 'alembic')
        abc_nodes = node_type.instances()

        for node in list(abc_nodes):

            instance = context.create_instance(name=node.name())
            instance.set_data('family', value='cache')
            instance.set_data('path', value=node.path())
            instance.add(node)
