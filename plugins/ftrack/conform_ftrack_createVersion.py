import pyblish.api
import shutil
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pyblish_utils

import ftrack

@pyblish.api.log
class ConformFtrackCreateVersion(pyblish.api.Conformer):
    """Publishes current workfile to a _Publish location, next to current working directory"""

    order = pyblish.api.Conformer.order + 0.1
    families = ['workFile']
    hosts = ['*']
    version = (0, 1, 0)
    optional = True

    def process_instance(self, instance):

        if instance.context.data('workfile_published'):
            if instance.context.data('create_ft_version'):
                self.log.info('CREATING VERSION')
                sourcePath = os.path.normpath(instance.data('published_path'))

                versionNumber = instance.context.data('version')

                taskid = instance.context.data('ft_context')['task']['id']
                task = ftrack.Task(taskid)

                shot = ftrack.Shot(id=instance.context.data('ft_context')['shot']['id'])

                assetType = instance.context.data('ft_context')['task']['code']
                assetName = instance.context.data('ft_context')['task']['type']

                asset = shot.createAsset(name=assetName, assetType=assetType, task=task)

                self.log.info('Using ftrack asset {}'.format(assetName))

                taskid = instance.context.data('ft_context')['task']['id']
                task = ftrack.Task(taskid)
                shot = ftrack.Shot(id=instance.context.data('ft_context')['shot']['id'])
                assetType = instance.context.data('ft_context')['task']['code']
                assetName = instance.context.data('ft_context')['task']['type']
                asset = shot.createAsset(name=assetName, assetType=assetType, task=task)


                version = asset.createVersion(comment='', taskid=taskid)
                if int(version.getVersion()) != int(versionNumber):
                    version.set('version', value=int(versionNumber))
                instance.context.set_data('create_ft_version', value=True)

                instance.context.set_data('ft_versionID', value=version.getId())
                print 'version: ' + str(version)
                version.publish()

        else:
            self.log.warning('Didn\'t create ftrack version because workfile wasn\'t published')
