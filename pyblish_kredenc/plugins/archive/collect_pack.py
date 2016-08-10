import pyblish.api
import pymel
from maya import cmds


@pyblish.api.log
class CollectPack(pyblish.api.Collector):
    """Inject all models from the scene into the context"""

    def process(self, context):

        sets = pymel.core.ls(sets=True)

        for obj in sets:

            patterns = ['pack']
            if any(ext in obj.name().lower() for ext in patterns):

                name = item = obj.name()

                name_list = None
                if '_' in name:
                    name_list = name.split('_')

                self.log.debug("name_list: {}".format(name_list))

                subset = ''
                if name_list:
                    if len(name_list) == 2:
                        name = name_list[0]
                        item = name
                    if len(name_list) == 3:
                        subset = name_list[0]
                        item = name_list[1]
                        name = subset + '_' + item

                self.log.debug("item {}, name {}, subset {}".format(item, name, subset))

                instance = context.create_instance(name, family="pack")

                instance.data['item'] = item
                instance.data['subset'] = subset


                self.log.debug("Collecting instance contents: {}".format(name))

                meshes = []
                roots = set()
                members = obj.members()

                cmds.select(members)

                instance[:] = cmds.file(exportSelected=True,
                                        preview=True,
                                        constructionHistory=True,
                                        force=True)

                files = pymel.core.ls(instance, type="file")
                textures = set()
                for f in files:
                    textures.add(f.fileTextureName.get())

                instance.data['textures'] = textures

                cmds.select( clear=True )

                self.log.info(textures)
