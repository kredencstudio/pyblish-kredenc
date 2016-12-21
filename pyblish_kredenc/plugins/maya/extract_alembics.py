import os
import pymel
import pyblish.api
import pyblish_kredenc.utils as pyblish_utils
from pyblish_kredenc.actions import actions_os

class ExtractAlembic(pyblish.api.Extractor):
    """Extracts alembic file to temp location.
    """

    families = ['alembic', 'cache', 'camera']
    optional = True
    actions = [actions_os.OpenOutputFolder, actions_os.OpenOutputFile]

    def process(self, instance):

        dir_path = pyblish_utils.temp_dir(instance)
        filename = "{0}.abc".format(instance.name)
        path = os.path.join(dir_path, filename)
        path = os.path.join(path).replace('\\', '/')
        self.log.debug('alembic extraction path: {}'.format(path))

        nodesString = ''

        roots = instance.data.get('roots')
        if not roots:
            roots = instance

        for node in roots:
            self.log.debug("root.." + str(node))
            try:
                nodesString += ' -root ' + node.name()
            except:
                nodesString += ' -root ' + node

        frame_start = int(pymel.core.playbackOptions(q=True, min=True))
        frame_end = int(pymel.core.playbackOptions(q=True, max=True))
        if instance.data['family'] == 'model':
            frame_end = frame_start

        cmd = '-frameRange %s %s' % (frame_start, frame_end)
        cmd += ' -uvWrite -worldSpace -wholeFrameGeo -dataFormat ogawa'
        cmd += ' -writeFaceSets -attr {}'.format('assetid')
        cmd += ' -eulerFilter -writeVisibility'
        cmd += ' -writeVisibility %s -file "%s"' % (nodesString, path)
        cmd += ' -attr innerRadius -attr outerRadius -attr attractionBias'
        cmd += ' -attr tipAttraction -attr baseAttraction'
        pymel.core.AbcExport(j=cmd)

        instance.data['outputPath_abc'] = path
