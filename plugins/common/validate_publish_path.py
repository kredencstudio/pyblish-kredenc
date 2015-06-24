import os
import pyblish.api

import ft_pathUtils
import ftrack

@pyblish.api.log
class ValidatePublishPath(pyblish.api.Validator):
    """Validates that the publish directory for the workFile exists"""

    families = ['workFile']
    version = (0, 1, 0)
    label = 'Check Publish Path'

    def process(self, context, instance):

        sourcePath = instance.data('path')
        directory, file = os.path.split(sourcePath)
        publishFolder = os.path.abspath(os.path.join(directory, '..', '_Publish'))

        version = context.data('version')
        version = 'v' + str(version).zfill(3)

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

        publishFile = ft_pathUtils.getPaths(taskid, templates, version)
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
