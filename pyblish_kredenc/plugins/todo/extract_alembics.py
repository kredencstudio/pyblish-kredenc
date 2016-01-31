import os
import re

import pymel
import pyblish.api
import ftrack


class ExtractAlembic(pyblish.api.Extractor):
    """
    """

    families = ['alembic']

    def get_path(self, instance):

        path = []
        filename = []

        '''
        GET FILENAME
        '''

        return os.path.join(*path).replace('\\', '/')

    def process(self, instance, context):

        root = instance[0]
        path = self.get_path(instance)

        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))

        nodesString = '-root ' + root.name()

        frame_start = int(pymel.core.playbackOptions(q=True, min=True))
        frame_end = int(pymel.core.playbackOptions(q=True, max=True))

        cmd = '-frameRange %s %s' % (frame_start, frame_end)
        cmd += ' -stripNamespaces -uvWrite -worldSpace -wholeFrameGeo '
        cmd += '-writeVisibility %s -file "%s"' % (nodesString, path)

        pymel.core.AbcExport(j=cmd)

        instance.data['extractDirAbc'] = path
