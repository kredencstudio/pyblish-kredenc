import pyblish.api
import shutil
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pyblish_utils

import ftrack
import ft_pathUtils


@pyblish.api.log
class ConformFtrackFlipbook(pyblish.api.Conformer):
    """Copies Preview movie to it's final location"""

    families = ['preview']
    hosts = ['*']
    version = (0, 1, 0)
    optional = True

    def process_instance(self, instance):

        if instance.has_data('output_path'):
            sourcePath = os.path.normpath(instance.data('output_path'))
            version = ''.join(pyblish_utils.version_get(instance.data('output_path'), 'v'))

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
                    'tv-ep-preview-file',
                ]
            elif 'Sequence' in parenttypes:
                templates = [
                    'tv-sq-preview-file',
                ]

            publishFile = ft_pathUtils.getPaths(taskid, templates, version)
            publishFile = os.path.normpath(publishFile[templates[0]])
            self.log.info('Copying preview to location: {}'.format(publishFile))

            shutil.copy(sourcePath, publishFile)
            instance.set_data('published_path', value=publishFile)
            instance.context.set_data('flipbook_published', value=True)
        else:
            self.log.warning('flipbook wasn\'t created so it can\'t be published')

