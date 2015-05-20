import pyblish.api
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pyblish_utils

import ftrack

@pyblish.api.log
class ConformFtrackUploadPreview(pyblish.api.Conformer):
    """Publishes current workfile to a _Publish location, next to current working directory"""

    order = pyblish.api.Conformer.order + 0.11
    families = ['preview']
    hosts = ['*']
    version = (0, 1, 0)
    optional = True

    def process_instance(self, instance):

        if instance.has_data('published_path'):
            sourcePath = os.path.normpath(instance.data('published_path'))
            # sourcePath = instance.data('path')
            version = None
            if instance.context.has_data('ft_versionID'):
                version = ftrack.AssetVersion(id=instance.context.data('ft_versionID'))


            #     (prefix, versionNumber) = pyblish_utils.version_get(sourcePath, 'v')

            #     taskid = instance.context.data('ft_context')['task']['id']
            #     task = ftrack.Task(taskid)
            #     shot = ftrack.Shot(id=instance.context.data('ft_context')['shot']['id'])
            #     assetType = instance.context.data('ft_context')['task']['code']
            #     assetName = instance.context.data('ft_context')['task']['type']
            #     asset = shot.createAsset(name=assetName, assetType=assetType, task=task)
            #     # creating version
            #     version = None
            #     for v in asset.getVersions():
            #         if int(v.getVersion()) == int(versionNumber):
            #             raise pyblish.api.ValidationError('This version already exists')
            #             version = v
            #
            #     if not version:
            #         version = asset.createVersion(comment='', taskid=taskid)
            #         if int(version.getVersion()) != int(versionNumber):
            #             raise pyblish.api.ValidationError('Version numbers don not match')
            #             version.set('version', value=int(versionNumber))
            #
            # version.publish()

                componentName = 'preview'

                try:
                    component = version.getComponent(name=componentName)
                    component.delete()
                    self.log.info('Replacing component with name "%s"' % componentName)
                except:
                    self.log.info('Creating component with name "%s"' % componentName)

                version.createComponent(name='preview', path=sourcePath)
                #make reviewable
                ftrack.Review.makeReviewable(version, sourcePath)
            else:
                self.log.info('No versionID found in context')

        else:
            self.log.warning('No published flipbook found!')
