import pyblish.api
import pymel


@pyblish.api.log
class CollectModel(pyblish.api.Collector):
    """Inject all models from the scene into the context"""

    def process(self, context):

        sets = pymel.core.ls(sets=True)

        for obj in sets:

            extensions = ['geo', 'geh', 'gep']
            if any(ext in obj.name().lower() for ext in extensions):

                name = obj.name()
                if '_' in name:
                    variation = name.split('_')[1].upper()
                else:
                    variation = name
                members = obj.members()
                nodes = []

                self.log.info("Collecting instance contents: {}".format(name))

                for mesh in pymel.core.ls(members, dag=True, exactType="mesh"):
                    nodes.append(mesh.getParent())

                self.log.info(nodes)
                instance = context.create_instance(name, family="model")
                instance.data['variation'] = variation
                instance[:] = nodes
                self.log.info("Model Variation: {}".format(variation))

                components = {}
                components[variation] = {'path': ''}
                instance.data['ftrackComponents'] = components

                self.log.info("Successfully collected %s" % name)
