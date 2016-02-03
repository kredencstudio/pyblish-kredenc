import shutil
import pyblish.api
import pyblish_kredenc.utils as pyblish_utils
from ft_studio import ft_pathUtils


@pyblish.api.log
class VersionUpWorkfile(pyblish.api.Conformer):
    """Versions up current workfile

    Expected data members:
    'ftrackData' - Necessary ftrack information gathered by select_ftrack
    """

    optional = True
    label = 'Version up scene'

    def process(self, context):

        if 'new_scene' in context:
            return

        if context.has_data('version'):

            sourcePath = context.data('currentFile')

            new_file = pyblish_utils.version_up(sourcePath)

            version = ''.join(pyblish_utils.version_get(new_file, 'v'))
            taskid = context.data('ftrackData')['Task']['id']

            ftrack_data = context.data['ftrackData']
            if 'Asset_Build' not in ftrack_data.keys():
                templates = [
                    'shot.work.file'
                ]
            else:
                templates = [
                    'asset.work.file'
                ]

            root = context.data('ftrackData')['Project']['root']
            self.log.debug(root)

            new_workFile = ft_pathUtils.getPathsYaml(taskid,
                                                     templateList=templates,
                                                     version=version,
                                                     root=root)[0]

            #################################################################

            self.log.info('New workfile version created: \
                            {}'.format(new_workFile))
            self.log.info('Next time you opens this task, \
                            start working on the version up file')

            shutil.copy(sourcePath, new_workFile)
            context.set_data('versionUpFile', value=new_workFile)

        else:
            raise pyblish.api.ValidationError(
                "Can't find versioned up filename in context. \
                workfile probably doesn't have a version.")
