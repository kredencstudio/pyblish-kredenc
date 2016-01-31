import os
import pymel
import pyblish.api
import pyblish_kredenc.utils as pyblish_utils
reload(pyblish_utils)


class ExtractAlembic(pyblish.api.Extractor):
    """Extracts alembic file to temp location.
    """

    families = ['alembic', 'model', 'cache', 'camera']
    optional = True

    def process(self, instance, context):

        self.log.info(pyblish_utils)
        dir_path = pyblish_utils.temp_dir(instance)
        filename = "{0}.abc".format(instance.name)
        path = os.path.join(dir_path, filename)
        path = os.path.join(path).replace('\\', '/')
        self.log.debug('alembic extraction path: {}'.format(path))

        nodesString = ''
        for node in instance:
            self.log.info("instance.." + str(node))
            try:
                nodesString += ' -root ' + node.name()
            except:
                nodesString += ' -root ' + node

        frame_start = int(pymel.core.playbackOptions(q=True, min=True))
        frame_end = int(pymel.core.playbackOptions(q=True, max=True))
        if instance.data['family'] == 'model':
            frame_end = frame_start

        cmd = '-frameRange %s %s' % (frame_start, frame_end)
        cmd += ' -noNormals -uvWrite -worldSpace -wholeFrameGeo -dataFormat ogawa'
        cmd += ' -writeVisibility %s -file "%s"' % (nodesString, path)

        pymel.core.AbcExport(j=cmd)

        instance.data['outputPath_abc'] = path
