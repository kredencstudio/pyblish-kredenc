import pymel.core as pm
import pyblish.api


class CollectCache(pyblish.api.ContextPlugin):
    """
    Collect Animation Caches
    """

    order = pyblish.api.CollectorOrder

    def transform_set(self, object_set):
        if not object_set.members():
            return False

        for member in object_set.members():
            if (member.nodeType() != "transform" and
               member.nodeType() != "objectSet"):
                return False

        return True

    def process(self, context):

        # FAMILY FILTERING

        sets = pm.ls(type="objectSet")

        for object_set in sets:

            if not self.transform_set(object_set):
                continue

            attrName = 'family'
            if hasattr(object_set, attrName):
                family_main = pm.Attribute(object_set.name() + "." + attrName).get(asString=1)
            else:
                continue

            if family_main == 'cache':

                ###################################
                # CACHE SPECIFIC COLLECTION

                # Remove illegal disk characters
                name = object_set.name().replace(":", "_")

                attrName = 'publish'
                if hasattr(object_set, attrName):
                    publish = pm.Attribute(object_set.name() + "." + attrName).get()
                else:
                    publish = True

                self.log.info("Set: {}".format(object_set))

                if ':' in object_set.name():
                    name = object_set.name().split(':')[0]
                else:
                    name = object_set.name().split('_')[0]

                members = object_set.members()
                nodes = []

                self.log.info("Collecting instance contents: {}".format(name))

                for mesh in members:
                    nodes.append(mesh)

                self.log.info(nodes)

                instance = context.create_instance(name)
                instance[:] = nodes
                instance.data["label"] = name + ' ' + family_main
                instance.data["publish"] = publish
                instance.data["family"] = family_main
                instance.data['families'] = [family_main, 'alembic']
                instance.data['item'] = name
                instance.data['subset'] = ''
                # instance.data['publish'] = False

                components = {}
                components[name] = {'path': ''}
                instance.data['ftrackComponents'] = components
