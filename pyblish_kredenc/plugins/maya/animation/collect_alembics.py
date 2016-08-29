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
                name = obj.name().split('_')[0]
                if ':' in name:
                    name = name.split(':')[0]

                members = obj.members()
                nodes = []


                self.log.info("Collecting instance contents: {}".format(name))

                for mesh in pymel.core.ls(members, dag=True, exactType='transform'):
                    nodes.append(mesh)

                self.log.info(nodes)

                instance = context.create_instance(name)
                instance[:] = nodes
                instance.data['families'] = ['cache']
                instance.data['item'] = name
                instance.data['subset'] = ''
                # instance.data['publish'] = False

                components = {}
                components[name] = {'path': ''}
                instance.data['ftrackComponents'] = components
