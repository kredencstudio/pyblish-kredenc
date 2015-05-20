import pyblish.api
import shutil
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pyblish_utils

import ftrack

@pyblish.api.log
class ValidateFtrackVersion(pyblish.api.Validator):
    """Publishes current workfile to a _Publish location, next to current working directory"""

    # order = pyblish.api.Conformer.order + 0.1
    families = ['workFile']
    hosts = ['*']
    version = (0, 1, 0)
    optional = True

    def process_instance(self, instance):

        if instance.context.has_data('version'):

            versionNumber = instance.context.data('version')

            taskid = instance.context.data('ft_context')['task']['id']
            task = ftrack.Task(taskid)

            shot = ftrack.Shot(id=instance.context.data('ft_context')['shot']['id'])

            assetType = instance.context.data('ft_context')['task']['code']
            assetName = instance.context.data('ft_context')['task']['type']

            asset = shot.createAsset(name=assetName, assetType=assetType, task=task)

            self.log.info('Using ftrack asset {}'.format(assetName))

            version = None
            for v in asset.getVersions():
                if int(v.getVersion()) == int(versionNumber):
                    if not v.get('ispublished'):
                        version = v
                        instance.context.set_data('ft_versionID', value=version.getId())
                        raise pyblish.api.ValidationError('This version already exists, but is not visible in ftrack UI.'
                                                    ' Repair to replace it. {}'.format(str(version)))
                    else:
                        version = v
                        instance.context.set_data('ft_versionID', value=version.getId())
                        raise pyblish.api.ValidationError('This version already exists Repair to replace it. '
                                                          '{}'.format(str(version)))


            print version
            if not version:
            #     version = asset.createVersion(comment='', taskid=taskid)
            #     if int(version.getVersion()) != int(versionNumber):
            #         version.set('version', value=int(versionNumber))
            #     instance.context.set_data('create_ft_version', value=True)
            #     self.log.info('Version will be created in conform step')
                instance.context.set_data('create_ft_version', value=True)
            #
            # version.publish()

        else:
            self.log.warning('Didn\'t create ftrack version because workfile wasn\'t published')

    def repair_instance(self, instance):
        """Saves the script
        """
        version = ftrack.AssetVersion(id=instance.context.data('ft_versionID'))
        version.delete()
        #repair
        pass