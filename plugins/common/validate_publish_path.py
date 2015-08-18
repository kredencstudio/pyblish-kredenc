import os
import pyblish.api
import sys

from ft_studio import ft_pathUtils
import ftrack
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pyblish_utils


@pyblish.api.log
class ValidatePublishPath(pyblish.api.Validator):
    """Validates that the publish directory for the workFile exists"""

    families = ['workFile']
    version = (0, 1, 0)
    label = 'Check Publish Path'

    def process(self, context, instance):

        sourcePath = os.path.normpath(context.data('currentFile'))
        directory, file = os.path.split(sourcePath)
        publishFolder = os.path.abspath(os.path.join(directory, '..', '_Publish'))

        # version = context.data('version')
        # prj_code = context.data('ftrackData')['Prcject']['code']
        # if prj_code in ['rad']:
        #     version = 'v' + str(version).zfill(3)
        # else:
        #     version = 'v' + str(version).zfill(2)

        version = ''.join(pyblish_utils.version_get(sourcePath, 'v'))
        self.log.debug(version)

        taskid = context.data('ftrackData')['Task']['id']
        self.log.debug(taskid)
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
        elif 'Asset Build' in parenttypes:
            templates = [
                'tv-asset-publish-file',
            ]

        self.log.debug(ft_pathUtils.__file__)

        publishFile = ft_pathUtils.getPaths(task, templates, version)

        publishFile = os.path.normpath(publishFile[templates[0]])

        if os.path.exists(publishFolder):
            context.set_data('publishFile', value=publishFile)
            context.set_data('deadlineInput', value=publishFile)
            self.log.debug('Setting publishFile: {}'.format(publishFile))
        else:
            name = instance
            msg = 'Publish directory for %s doesn\'t exists' % name

            raise ValueError(msg)


    def repair(self, instance):
        """Auto-repair creates the output directory"""
        path = os.path.dirname(instance[0]['file'].value())

        if not os.path.exists(path):
            os.makedirs(path)
