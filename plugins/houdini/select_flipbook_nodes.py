import hou
import pyblish.api


@pyblish.api.log
class SelectFlipbookNodes(pyblish.api.Selector):
    """Selects all flipbook nodes"""

    hosts = ['houdini']
    version = (0, 1, 0)

    def process(self, context):

        renderNode = hou.node( "/out" )
        render_nodes = renderNode.children()

        for node in list(render_nodes):

            if 'flipbook' in node.type().name():
                instance = context.create_instance(name=node.name())
                instance.set_data('family', value='preview')

                instance.add(node)

                output = instance[0].parm('outputV').eval()

                # ftrack data
                components = {'preview': {'path': output,
                                          'reviewable': True,
                                          }}
                instance.set_data('ftrackComponents', value=components)