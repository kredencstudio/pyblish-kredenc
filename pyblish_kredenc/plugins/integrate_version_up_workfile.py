import shutil
import pyblish.api
import pyblish_kredenc.utils as pyblish_utils
from ftrack_kredenc import ft_pathUtils


@pyblish.api.log
class VersionUpWorkfile(pyblish.api.InstancePlugin):
    """Versions up current workfile

    Expected data members:
    'ftrackData' - Necessary ftrack information gathered by select_ftrack
    """
    order = pyblish.api.IntegratorOrder
    optional = True
    families = ['scene']
    label = 'Version up scene'

    def process(self, instance):

        if 'new_scene' in instance.context:
            return

        if instance.context.has_data('version'):

            sourcePath = instance.context.data('currentFile')

            new_file = pyblish_utils.version_up(sourcePath)

            version = ''.join(pyblish_utils.version_get(new_file, 'v'))
            taskid = instance.context.data('ftrackData')['Task']['id']

            ftrack_data = instance.context.data['ftrackData']
            if 'Asset_Build' not in ftrack_data.keys():
                templates = [
                    'shot.work.scene'
                ]
            else:
                templates = [
                    'asset.work.scene'
                ]

            root = instance.context.data('ftrackData')['Project']['root']
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
            instance.context.set_data('versionUpFile', value=new_workFile)

        else:
            raise pyblish.api.ValidationError(
                "Can't find versioned up filename in instance.context. \
                workfile probably doesn't have a version.")
