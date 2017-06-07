import pyblish.api
import shutil
import os



@pyblish.api.log
class IntegratePack(pyblish.api.Integrator):
    """Inject all models from the scene into the context"""

    families = ['pack']

    def process(self, instance):

        publish_path = instance.data['publishFile']

        for f in instance.data['textures']:
            if os.path.isfile(f):
                new_tex = os.path.join(os.path.dirname(publish_path), os.path.basename(f))
                output = shutil.copy(f, new_tex)

        output_path = instance.data.get['outputPath']

        if output_path and publish_path:
            if not os.path.exists(os.path.dirname(publish_path)):
                os.mkdirs(os.path.dirname(publish_path))

            self.log.info('Copying model from location: {}'.format(output_path))
            self.log.info('Copying model to location: {}'.format(publish_path))
            shutil.copy(sourcePath, publishFile)
