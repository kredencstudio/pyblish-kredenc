import pyblish.api
from maya import cmds

import pyblish_magenta.utils.maya.mesh as mesh_utils


class ValidateMeshNonZeroFaceArea(pyblish.api.Validator):
    """Validate meshes don't have zero area faces.

    .. note:: This can be slow for high-res meshes.

    Also see: http://help.autodesk.com/view/MAYAUL/2015/ENU/?guid=Mesh__Cleanup

    Check is based on Maya's polyCleanup *'Faces with zero geometry area'* script.

    """

    families = ['model']
    hosts = ['maya']
    category = 'geometry'
    version = (0, 1, 0)
    label = 'Mesh Face Area Non Zero'

    __tolerance = 1e-8

    def process(self, instance):
        """Process all meshes"""
        meshes = instance.data['shapes']

        # Get all faces
        faces = ['{0}.f[*]'.format(node) for node in meshes]

        # Filter by constraint on face area
        invalid = mesh_utils.polyConstraint(faces,
                                            disable=True,  # Disable previous settings, use only current
                                            t=0x0008,      # type: 0x0008(face)
                                            geometricarea=1,
                                            geometricareabound=(0, self.__tolerance))

        if invalid:
            raise RuntimeError("Meshes found with zero face areas: {0}".format(invalid))
