try:
    import sys

    args = sys.argv
    file_to_read = args[1]
    file_to_save = args[2]
except:
    pass

import os
import maya.standalone
maya.standalone.initialize('Python')

from maya import cmds, mel
cmds.file(file_to_read, o=True)

files = cmds.ls(type="file")

for f in files:
    tex = os.path.basename(cmds.getAttr(f + '.fileTextureName'))
    cmds.setAttr(f + '.fileTextureName', tex, type='string')

cmds.loadPlugin("fbxmaya")

mel.eval('FBXResetExport')
mel.eval('FBXExportFileVersion "FBX201400"')
mel.eval('FBXExportInputConnections -v 1')
mel.eval('FBXExportConstraints -v 0')
mel.eval('FBXExportUseSceneName -v 1')
mel.eval('FBXExportInAscii -v 0')
mel.eval('FBXExportSkins -v 1')
mel.eval('FBXExportShapes -v 1')
mel.eval('FBXExportCameras -v 1')
mel.eval('FBXExportLights -v 0')
mel.eval('FBXExportBakeComplexAnimation -v 0')
# export selection
cmds.FBXExport('-file', '{}'.format(file_to_save))

os.remove(file_to_read)
