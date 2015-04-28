import os
import tempfile
import subprocess
import getpass

import nuke
import nukescripts
import pyblish.api
import shutil


@pyblish.api.log
class extractWorkfile(pyblish.api.Extractor):
    """Publishes current workfile to a _Publish location, next to current working directory"""

    families = ['workfile']
    hosts = ['nuke']
    version = (0, 1, 0)
    optional = True

    def process_instance(self, instance):
        # submitting job
        sourcePath = instance.data('path')
        directory, file = os.path.split(sourcePath)
        publishPath = os.path.abspath(os.path.join(directory, '..', '_Publish', file))
        shutil.copy(sourcePath, publishPath)