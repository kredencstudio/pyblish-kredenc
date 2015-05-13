import hou
import pyblish.api


@pyblish.api.log
class SelectFlipbookNodes(pyblish.api.Selector):
    """Selects all flipbook nodes"""

    hosts = ['houdini']
    version = (0, 1, 0)

    def process_context(self, context):

        renderNode = hou.node( "/out" )
        render_nodes = renderNode.children()

        for node in list(render_nodes):

            if 'flipbook' in node.type().name():
                instance = context.create_instance(name=node.name())
                instance.set_data('family', value='preview')
                # instance.set_data('output_path', value=node.parm('outputV').eval())

                instance.add(node)
