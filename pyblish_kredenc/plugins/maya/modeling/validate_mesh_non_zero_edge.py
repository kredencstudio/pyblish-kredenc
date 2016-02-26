import pyblish.api
from maya import cmds

import pyblish_magenta.utils.maya.mesh as mesh_utils


class ValidateMeshNonZeroEdges(pyblish.api.Validator):
    """Validate meshes don't have edges with a zero length.

    Also see: http://help.autodesk.com/view/MAYAUL/2015/ENU/?guid=Mesh__Cleanup

    Check is based on Maya's polyCleanup *'Edges with zero length'* script.

    """

    families = ['model']
    hosts = ['maya']
    category = 'geometry'
    version = (0, 1, 0)
    label = 'Mesh Non Zero Edges'

    __tolerance = 1e-5

    def process(self, instance):
        """Process all the nodes in the instance 'objectSet'"""
        meshes = instance.data['shapes']

        # Get all edges
        edges = ['{0}.e[*]'.format(node) for node in meshes]

        # Filter by constraint on edge length
        invalid = mesh_utils.polyConstraint(edges,
                                            disable=True,  # Disable previous settings, use only current
                                            t=0x8000,      # type: 0x8000(edge)
                                            length=1,
                                            lengthbound=(0, self.__tolerance))

        if invalid:
            raise RuntimeError("Meshes found with zero edge length: {0}".format(invalid))
