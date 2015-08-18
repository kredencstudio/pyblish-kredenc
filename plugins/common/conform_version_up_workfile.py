import sys
import shutil
import os
import pyblish.api

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pyblish_utils

import ftrack
from ft_studio import ft_pathUtils

@pyblish.api.log
class VersionUpWorkfile(pyblish.api.Conformer):
    """Versions up current workfile

    Expected data members:
    'ftrackData' - Necessary ftrack information gathered by select_ftrack
    """

    families = ['workFile']
    version = (0, 1, 0)
    optional = True
    label = 'Version up currentFile'

    def process(self, context, instance):

        if context.has_data('version'):

            sourcePath = os.path.normpath(context.data('currentFile'))

            ######################################################################################
            # TODO: figure out how to make path matching customisable
            ####

            new_file = pyblish_utils.version_up(sourcePath)

            version = ''.join(pyblish_utils.version_get(new_file, 'v'))
            taskid = context.data('ftrackData')['Task']['id']
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
                    'tv-ep-work-file',
                ]
            elif 'Sequence' in parenttypes:
                templates = [
                    'tv-sq-work-file',
                ]
            elif 'Asset Build' in parenttypes:
                templates = [
                    'tv-asset-work-file',
                ]

            new_workFile = ft_pathUtils.getPaths(task, templates, version)
            new_workFile = os.path.normpath(new_workFile[templates[0]])

            ######################################################################################

            self.log.info('New workfile version created: {}'.format(new_workFile))
            self.log.info('Next time you opens this task, start working on the version up file')

            shutil.copy(sourcePath, new_workFile)
            context.set_data('versionUpFile', value=new_workFile)

        else:
            raise pyblish.api.ValidationError("Can't find versioned up filename in context. "
                                              "workfile probably doesn't have a version.")
