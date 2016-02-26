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

                self.log.info("name_list: {}".format(name_list))

                subset = None
                if name_list:
                    if len(name_list) == 2:
                        name = name_list[1]
                        item = name
                    if len(name_list) == 3:
                        subset = name_list[0]
                        item = name_list[2]
                        name = subset + '_' + item


                instance = context.create_instance(name, family="model")

                instance.data['item'] = item

                self.log.info("Collecting instance contents: {}".format(name))
                nodes = []
                members = obj.members()

                for mesh in pymel.core.ls(members, dag=True, exactType="mesh"):
                    nodes.append(mesh.getParent())
                self.log.info(nodes)
                instance[:] = nodes

                if subset:
                    instance.data['subset'] = subset
                    self.log.info("Model subset: {}".format(subset))

                components = {}
                instance.data['ftrackComponents'] = components

                self.log.info("Successfully collected %s" % name)
