import pyblish.api
import shutil
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pyblish_utils

import ft_pathUtils


@pyblish.api.log
class ConformFtrackFlipbook(pyblish.api.Conformer):
    """Publishes current workfile to a _Publish location, next to current working directory"""

    families = ['preview']
    hosts = ['houdini']
    version = (0, 1, 0)
    optional = True

    def process_instance(self, instance):
        # submitting job
        sourcePath = os.path.normpath(instance.data('output_path'))


        version = ''.join(pyblish_utils.version_get(instance.data('output_path'), 'v'))

        templates = ['tv-ep-preview-file']

        publishFile = ft_pathUtils.getPaths(instance.context.data('ft_context')['task']['id'], templates, version)
        print publishFile
        publishFile = os.path.normpath(publishFile[templates[0]])

        shutil.copy(sourcePath, publishFile)
        instance.context.set_data('flipbook_published', value=True)
