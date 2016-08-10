import pyblish.api
import pymel
# from maya import cmds


@pyblish.api.log
class ValidatePack(pyblish.api.Validator):
    """Inject all models from the scene into the context"""

    order = pyblish.api.Validator.order
    families = ['pack']

    def process(self, instance):

        files = pymel.core.ls(instance, type="file")
        textures = set()
        for f in files:
            textures.add(f.fileTextureName.get())

        instance.data['textures'] = textures

        self.log.info(textures)
