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
    """Copies current workfile to it's final location"""

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
        publishFile = os.path.normpath(publishFile[templates[0]])

        self.log.info('Copying Workfile to location: {}'.format(publishFile))

        shutil.copy(sourcePath, publishFile)
        instance.set_data('published_path', value=publishFile)
        instance.context.set_data('workfile_published', value=True)
