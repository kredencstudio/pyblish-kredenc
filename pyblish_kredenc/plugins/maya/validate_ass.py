import pyblish.api
import pyblish_kredenc.utils as pyblish_utils
reload(pyblish_utils)
import os


class ValidateAss(pyblish.api.InstancePlugin):
    """Extracts arnold archive file.
    """
    order = pyblish.api.ValidatorOrder
    families = ['ass']
    optional = True

    def process(self, instance):

        dir_path = pyblish_utils.temp_dir(instance)
        outputFrames = instance.data['outputFilename']
        folder, filename = os.path.split(outputFrames)
        basename, ext = os.path.splitext(os.path.splitext(filename)[0])

        output_path = os.path.join(dir_path, 'ass', basename + '.ass')
        instance.data['outputPath_ass'] = output_path
        self.log.debug('output_path: {}'.format(output_path))

        start_frame = instance.data['startFrame'].zfill(instance.data['padding'])
        frameFileName = '{}.{}.ass'.format(basename, start_frame)
        publish_file = os.path.join(folder, 'ass', frameFileName)
        instance.data['publishFile'] = publish_file
        self.log.debug('publish_file: {}'.format(publish_file))
