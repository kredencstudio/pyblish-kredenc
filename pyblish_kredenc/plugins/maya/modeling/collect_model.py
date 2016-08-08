import pyblish.api
import pymel


@pyblish.api.log
class CollectModel(pyblish.api.Collector):
    """Inject all models from the scene into the context"""

    def process(self, context):

        sets = pymel.core.ls(sets=True)

        for obj in sets:

            patterns = ['geo', 'hires', 'proxy', 'geh', 'gep', 'lod']
            if any(ext in obj.name().lower() for ext in patterns):

                name = item = obj.name()

                name_list = None
                if '_' in name:
                    name_list = name.split('_')

                self.log.debug("name_list: {}".format(name_list))

                subset = None
                if name_list:
                    if len(name_list) == 2:
                        name = name_list[0]
                        item = name
                    if len(name_list) == 3:
                        subset = name_list[0]
                        item = name_list[1]
                        name = subset + '_' + item

                self.log.debug("item {}, name {}, subset {}".format(item, name, subset))

                instance = context.create_instance(name, family="model")
                instance.data['families'] = ['model', 'alembic']

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

                if subset:
                    instance.data['subset'] = subset
                    self.log.debug("Model subset: {}".format(subset))

                components = {}
                instance.data['ftrackComponents'] = components

                self.log.info("Successfully collected %s" % name)
