import pyblish.api
from maya import cmds

@pyblish.api.log
class ValidateMeshLaminaFaces(pyblish.api.Validator):
    """Validate meshes don't have lamina faces.

    Lamina faces share all of their edges.

    """

    families = ['model']
    hosts = ['maya']
    optional = True
    label = 'Mesh Lamina Faces'

    def process(self, instance):
        """Process all the nodes in the instance 'objectSet'"""

        meshes = instance.data['shapes']

        invalid = []
        for mesh in meshes:
            self.log.info('checking: {}'.format(mesh))
            if cmds.polyInfo(mesh, laminaFaces=True):
                invalid.append(mesh)

        if invalid:
            raise ValueError("Meshes found with lamina faces: {0}".format(invalid))
