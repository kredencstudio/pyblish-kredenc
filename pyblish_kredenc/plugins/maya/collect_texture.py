import os

import pyblish.api
import pymel.core as pm


class CollectTexture(pyblish.api.Collector):
    """
    """

    def process(self, context):

        for node in pm.ls(type='file'):
            textureName = node.fileTextureName.get()

            if node.isReferenced():
                continue

            if not textureName:
                continue

            if not os.path.exists(textureName):
                continue

            name = os.path.basename(textureName)
            instance = context.create_instance(name=name)
            instance.set_data('family', value='texture')
            instance.add(node)
