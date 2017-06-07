import pyblish.api
import os


@pyblish.api.log
class IntegrateTaskFolders(pyblish.api.Integrator):
    """Creates task folders if non-existent
    """

    families = ['new_scene']
    optional = True
    label = 'Task Folders'

    def process(self, instance):

        if 'workfile' in instance.context.data:

            workfile = instance.context.data['workfile']
            workFolder = os.path.dirname(workfile)
            # publishFolder = os.path.join(os.path.dirname(workFolder), 'publish')
            version = instance.context.data['version']
            version = 'v' + str(version).zfill(2)
            self.log.debug(version)

            if not os.path.exists(workFolder):
                os.makedirs(workFolder)
                self.log.info('Task Folders Prepared: \
                              {}'.format(workFolder))

            # if not os.path.exists(publishFolder):
            #     os.makedirs(publishFolder)
            #     self.log.info('Task Folders Prepared: \
            #                   {}'.format(publishFolder))

        else:
            raise pyblish.api.ValidationError(
                "Can't find versioned up filename in instance.context. \
                workfile probably doesn't have a version.")
