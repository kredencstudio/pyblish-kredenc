import pyblish.api
from maya import cmds


class ValidateMeshNonManifold(pyblish.api.Validator):
    """Ensure that meshes don't have non-manifold edges or vertices"""

    families = ['model']
    hosts = ['maya']
    category = 'geometry'
    optional = True
    version = (0, 1, 0)
    label = 'Mesh Non-Manifold Vertices/Edges'

    def process(self, instance):
        """Process all the nodes in the instance 'objectSet'"""
        meshes = instance.data['shapes']

        invalid = []
        for mesh in meshes:
            if cmds.polyInfo(mesh, nonManifoldVertices=True) or cmds.polyInfo(mesh, nonManifoldEdges=True):
                invalid.append(mesh)

        if invalid:
            raise ValueError("Meshes found with non-manifold edges/vertices: {0}".format(invalid))
