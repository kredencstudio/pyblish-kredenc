import pyblish.api
import pymel


class CollectLook(pyblish.api.ContextPlugin):
    """Collects current workfile"""

    order = pyblish.api.CollectorOrder
    label = 'Look'

    def process(self, context):

        sets = pymel.core.ls(sets=True)

        for obj in sets:

            patterns = ['look']
            if any(ext in obj.name().lower() for ext in patterns):

                name_list = None
                if '_' in obj.name():
                    name_list = obj.name().split('_')

                self.log.debug("name_list: {}".format(name_list))

                subset = None
                if name_list:
                    if len(name_list) == 2:
                        item = 'base'
                    if len(name_list) == 3:
                        item = name_list[0]

                name = item + '_look'

                self.log.debug("item {}, subset {}".format(name, subset))

                instance = context.create_instance(name, family='look')
                instance.data['families'] = ['look']
                instance.data['item'] = item

                self.log.debug("Collecting instance contents: {}".format(name))
                nodes = []
                meshes = []
                roots = set()
                members = obj.members()

                for mesh in pymel.core.ls(members, dag=True, l=True, exactType="transform"):
                    nodes.append(mesh.name())
                    shape = mesh.getShape()
                    if shape:
                        meshes.append(shape.fullPath())
                    roots.add(mesh.root())

                self.log.debug('nodes: {}'.format(nodes))
                self.log.debug('meshes: {}'.format(meshes))
                self.log.debug('roots: {}'.format(roots))
                instance[:] = nodes
                instance.data['roots'] = list(roots)
                instance.data['shapes'] = list(meshes)

                components = {}
                instance.data['ftrackComponents'] = components

                self.log.info("Successfully collected %s" % name)
