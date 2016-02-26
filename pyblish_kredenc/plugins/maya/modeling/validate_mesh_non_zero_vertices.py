import pyblish.api
import pyblish_maya
from maya import cmds


class ValidateMeshNonZeroVertices(pyblish.api.Validator):
    """Validate meshes have no internal points offsets (#34)

    Vertices can have internal vertex offset that mess with subsequent
    deformers and are difficult to track down. The offset values can be seen
    in the channelBox when selecting the vertices, all values there should be
    zero.
    """

    families = ['model']
    hosts = ['maya']
    category = 'geometry'
    version = (0, 1, 0)
    label = 'Mesh Non Zero Vertices'

    __tolerance = 1e-8

    def _iter_internal_pts(self, mesh):
        """Yield the internal offset values for each point of the mesh"""
        num_pts = cmds.getAttr('{0}.pnts'.format(mesh), size=True)
        for i in range(num_pts):
            attr = '{0}.pnts[{1}]'.format(mesh, i)
            yield cmds.getAttr(attr)[0]

    def is_invalid(self, mesh):
        pts = self._iter_internal_pts(mesh)
        for pt in pts:
            if any(abs(v) > self.__tolerance for v in pt):
                return True
        return False

    def process(self, instance):
        """Process all meshes"""
        meshes = instance.data['shapes']

        invalid = [mesh for mesh in meshes if self.is_invalid(mesh)]
        if invalid:
            raise RuntimeError("Meshes found with non-zero vertices: "
                               "{0}".format(invalid))

    def repair(self, instance):
        """Repair the meshes by 'baking' offsets into the input mesh"""
        meshes = instance.data['shapes']
        invalid = [mesh for mesh in meshes if self.is_invalid(mesh)]

        # TODO: Find a better way to reset values whilst preserving offsets
        with pyblish_maya.maintained_selection():
            for mesh in invalid:
                cmds.polyMoveVertex(mesh, constructionHistory=False)
