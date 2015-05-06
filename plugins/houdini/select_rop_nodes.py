import hou
import pyblish.api


@pyblish.api.log
class SelectRopNodes(pyblish.api.Selector):
    """Selects all write nodes"""

    hosts = ['*']
    version = (0, 1, 0)

    def upstream_nodes(self, node, results=[]):
        if node.dependencies():
            results.extend(node.dependencies())
            for n in node.dependencies():
                return self.upstream_nodes(n)

        return results

    def process_context(self, context):

        renderNode = hou.node( "/out" )
        render_nodes = renderNode.children()

        # render_nodes = []
        # for rop in renderers:
        #     render_nodes.append( rop.name() )


        for node in list(render_nodes):
            instance = context.create_instance(name=node.name())
            instance.set_data('family', value='rops')
            instance.add(node)
