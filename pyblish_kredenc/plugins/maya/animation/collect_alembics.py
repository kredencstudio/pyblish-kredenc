import pymel
import pyblish.api


class CollectCache(pyblish.api.ContextPlugin):
    """
    Collect Animation Caches
    """

    order = pyblish.api.CollectorOrder

    def process(self, context):

        sets = pymel.core.ls(sets=True)

        for obj in sets:

            extensions = ['cache']

            if any(ext in obj.name().lower() for ext in extensions):

                self.log.info("Set: {}".format(obj))

                if ':' in obj.name():
                    name = obj.name().split(':')[0]
                    # name = name.replace(':', '-')

                members = obj.members()
                nodes = []


                self.log.info("Collecting instance contents: {}".format(name))

                for mesh in members:
                    nodes.append(mesh)

                self.log.info(nodes)

                instance = context.create_instance(name)
                instance[:] = nodes
                instance.data['family'] = 'cache'
                instance.data['families'] = ['cache']
                instance.data['item'] = name
                instance.data['subset'] = ''
                # instance.data['publish'] = False

                components = {}
                components[name] = {'path': ''}
                instance.data['ftrackComponents'] = components
