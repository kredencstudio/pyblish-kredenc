import pyblish.api
import pymel


@pyblish.api.log
class CollectSets(pyblish.api.Collector):
    """Inject all models from the scene into the context"""

    def transform_set(self, object_set):
        if not object_set.members():
            return False

        for member in object_set.members():
            if (member.nodeType() != "transform"):
                return False

        return True

    def process(self, context):

        # FAMILY FILTERING

        sets = pymel.core.ls(type="objectSet")

        for object_set in sets:

            if not self.transform_set(object_set):
                continue

            attrName = 'family'
            if hasattr(object_set, attrName):
                family_main = pymel.core.Attribute(object_set.name() + "." + attrName).get(asString=1)
                self.log.debug("found supported asset: {}".format(family_main))
            else:
                continue

            if family_main in ['model', 'rig', 'look']:

                # Remove illegal disk characters
                name = object_set.name().replace(":", "_")

                attrName = 'publish'
                if not hasattr(object_set, attrName):
                    pymel.core.addAttr(
                        object_set,
                        longName=attrName,
                        at='bool'
                    )
                publish = pymel.core.Attribute(object_set.name() + "." + attrName).get()

                item = name

                name_list = None
                if '_' in name:
                    name_list = name.split('_')

                subset = None
                if name_list:
                    if len(name_list) == 2:
                        item = name_list[0]
                    if len(name_list) == 3:
                        subset = name_list[0]
                        item = name_list[1]

                self.log.debug("item {}, name {}, subset {}".format(item, name, subset))

                instance = context.create_instance(name=name)
                instance.add(object_set)
                instance.data["label"] = item + ' ' + family_main
                instance.data["publish"] = publish
                instance.data["family"] = family_main
                instance.data['families'] = [family_main]

                if family_main in ['model']:
                    instance.data['families'].append('alembic')

                instance.data['item'] = item

                self.log.debug("Collecting instance contents: {}".format(name))
                nodes = []
                meshes = []
                roots = set(object_set.members())

                for mesh in pymel.core.ls(roots, dag=True, l=True, exactType="transform"):
                    nodes.append(mesh.name())
                    shape = mesh.getShape()
                    if shape:
                        meshes.append(shape.fullPath())

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
