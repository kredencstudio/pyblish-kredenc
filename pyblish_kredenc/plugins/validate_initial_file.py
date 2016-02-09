import pyblish.api
from ft_studio import ft_pathUtils


@pyblish.api.log
class ValidateInitialScene(pyblish.api.InstancePlugin):
    """Checks if we are able to create new workfile
    """
    order = pyblish.api.ValidatorOrder
    families = ['new_scene']
    label = 'Initial scene'

    def process(self, instance):

        if instance.context.has_data('version'):

            version = instance.context.data['version']
            version = 'v' + str(version).zfill(3)
            self.log.debug(version)

            taskid = instance.context.data('ftrackData')['Task']['id']
            self.log.debug(taskid)

            root = instance.context.data('ftrackData')['Project']['root']
            self.log.debug(root)

            ftrack_data = instance.context.data['ftrackData']
            if 'Asset_Build' in ftrack_data.keys():
                templates = [
                    'asset.work.file'
                ]
            else:
                templates = [
                    'shot.work.file'
                ]


            self.log.debug(templates)

            new_workFile = ft_pathUtils.getPathsYaml(taskid,
                                                     templateList=templates,
                                                     version=version,
                                                     root=root)[0]

            instance.context.data['workfile'] = new_workFile

            self.log.info('New workfile path prepared: \
                            {}'.format(new_workFile))

        else:
            raise pyblish.api.ValidationError(
                "Can't find versioned up filename in instance.context. \
                workfile probably doesn't have a version.")
