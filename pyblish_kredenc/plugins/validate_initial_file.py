import pyblish.api
from ft_studio import ft_pathUtils


@pyblish.api.log
class ValidateInitialScene(pyblish.api.Validator):
    """Versions up current workfile

    Expected data members:
    'ftrackData' - Necessary ftrack information gathered by select_ftrack
    """

    families = ['new_scene']
    optional = True
    label = 'Initial scene'

    def process(self, context, instance):

        if context.has_data('version'):

            version = context.data['version']
            version = 'v' + str(version).zfill(3)
            self.log.debug(version)

            taskid = context.data('ftrackData')['Task']['id']
            self.log.debug(taskid)

            root = context.data('ftrackData')['Project']['root']
            self.log.debug(root)

            ftrack_data = context.data['ftrackData']
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

            context.data['workfile'] = new_workFile

            self.log.info('New workfile path prepared: \
                            {}'.format(new_workFile))

        else:
            raise pyblish.api.ValidationError(
                "Can't find versioned up filename in context. \
                workfile probably doesn't have a version.")
