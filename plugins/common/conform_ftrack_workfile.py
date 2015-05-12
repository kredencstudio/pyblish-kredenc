import pyblish.api
import shutil
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pyblish_utils

import ftrack
import ft_pathUtils


@pyblish.api.log
class ConformFtrackWorkfile(pyblish.api.Conformer):
    """Publishes current workfile to a _Publish location, next to current working directory"""

    families = ['workFile']
    hosts = ['*']
    version = (0, 1, 0)
    optional = True

    def process_instance(self, instance):
        sourcePath = os.path.normpath(instance.data('path'))

        version = ''.join(pyblish_utils.version_get(instance.context.data('current_file'), 'v'))

        taskid = instance.context.data('ft_context')['task']['id']
        task = ftrack.Task(taskid)
        parents = task.getParents()

        # Prepare data for parent filtering
        parenttypes = []
        for parent in parents:
            try:
                parenttypes.append(parent.get('objecttypename'))
            except:
                pass

        print parenttypes
        # choose correct template
        if 'Episode' in parenttypes:
            templates = [
                'tv-ep-publish-file',
            ]
        elif 'Sequence' in parenttypes:
            templates = [
                'tv-sq-publish-file',
            ]

        publishFile = ft_pathUtils.getPaths(taskid, templates, version)
        print publishFile
        publishFile = os.path.normpath(publishFile[templates[0]])

        shutil.copy(sourcePath, publishFile)
        instance.context.set_data('workfile_published', value=True)
