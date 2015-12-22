import pyblish.api
import os


@pyblish.api.log
class IntegrateTaskFolders(pyblish.api.Integrator):
    """Versions up current workfile

    Expected data members:
    'ftrackData' - Necessary ftrack information gathered by select_ftrack
    """

    families = ['new_scene']
    optional = True
    label = 'Task Folders'

    def process(self, context, instance):

        if 'workfile' in context.data:

            workfile = context.data['workfile']
            workFolder = os.path.dirname(workfile)
            publishFolder = os.path.join(os.path.dirname(workFolder), 'publish')
            version = context.data['version']
            version = 'v' + str(version).zfill(3)
            self.log.debug(version)

            if not os.path.exists(workFolder):
                os.makedirs(workFolder)
                self.log.info('Task Folders Prepared: \
                              {}'.format(workFolder))

            if not os.path.exists(publishFolder):
                os.makedirs(publishFolder)
                self.log.info('Task Folders Prepared: \
                              {}'.format(publishFolder))

        else:
            raise pyblish.api.ValidationError(
                "Can't find versioned up filename in context. \
                workfile probably doesn't have a version.")
