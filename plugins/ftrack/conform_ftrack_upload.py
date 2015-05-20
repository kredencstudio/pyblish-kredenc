import pyblish.api
import shutil
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pyblish_utils

import ftrack

@pyblish.api.log
class ConformFtrackUpload(pyblish.api.Conformer):
    """Publishes current workfile to a _Publish location, next to current working directory"""

    order = pyblish.api.Conformer.order + 0.11
    families = ['workFile']
    hosts = ['*']
    version = (0, 1, 0)
    optional = True

    def process_instance(self, instance):

        if instance.context.data('workfile_published'):
            sourcePath = os.path.normpath(instance.data('published_path'))

            if instance.context.has_data('ft_versionID'):
                version = ftrack.AssetVersion(id=instance.context.data('ft_versionID'))

                # (prefix, versionNumber) = pyblish_utils.version_get(sourcePath, 'v')

                # taskid = instance.context.data('ft_context')['task']['id']
                # task = ftrack.Task(taskid)
                #
                # shot = ftrack.Shot(id=instance.context.data('ft_context')['shot']['id'])
                #
                # assetType = instance.context.data('ft_context')['task']['code']
                # assetName = instance.context.data('ft_context')['task']['type']
                # asset = shot.createAsset(name=assetName, assetType=assetType, task=task)
                # self.log.info('Using ftrack asset {}'.format(assetName))
                # # creating version
                # print int(versionNumber)
                # version = None
                # for v in asset.getVersions():
                #     if int(v.getVersion()) == int(versionNumber):
                #         if v.get('ispublished'):
                #             pyblish.api.ValidationError('This version already exists, please delete it ')
                #         else:
                #             version = v
                #
                # if not version:
                #     version = asset.createVersion(comment='', taskid=taskid)
                #     print version.getVersion()
                #     print versionNumber
                #     if int(version.getVersion()) != int(versionNumber):
                #         raise pyblish.api.ValidationError('Version numbers don not match')
                #         version.set('version', value=int(versionNumber))
                #
                # self.log.info('Using ftrack version {} - {}'.format(assetName, versionNumber))
                #
                # version.publish()

                componentName = 'scene'

                try:
                    component = version.getComponent(name=componentName)
                    component.delete()
                    self.log.info('Replacing component with name "%s"' % componentName)
                except:
                    self.log.info('Creating component with name "%s"' % componentName)

                version.createComponent(name=componentName, path=sourcePath)
                self.log.info('Component {} created'.format(componentName))
            else:
                self.log.info('No versionID found in context')
                # instance.context.set_data('ft_versionID', value=version.getId())
        else:
            self.log.warning('Didn\'t create ftrack version because workfile wasn\'t published')
