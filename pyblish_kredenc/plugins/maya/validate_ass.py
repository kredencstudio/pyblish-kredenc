import pyblish.api
import pyblish_kredenc.utils as pyblish_utils
# reload(utils)
import os
import shutil


class RemovePreviousAssFiles(pyblish.api.Action):
    label = "Remove previous ass files"
    on = "failed"
    icon = "trash"

    def process(self, context, plugin):

        instances = pyblish_utils.filter_instances(context, plugin)

        for instance in instances:
            if instance.data.get('publishFile') and 'arnold' in instance.data['families']:
                publish_folder = os.path.split(instance.data['publishFile'])[0]
                shutil.rmtree(publish_folder)


class Ass(pyblish.api.InstancePlugin):
    """Extracts arnold archive file.
    """

    order = pyblish.api.ValidatorOrder + 0.2
    families = ['arnold']
    optional = True
    label = 'Validate Ass'

    actions = [RemovePreviousAssFiles]

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

        output_folder = os.path.split(output_path)[0]
        self.log.debug('outputFolder: {}'.format(output_folder))

        publish_folder = os.path.split(publish_file)[0]
        self.log.debug('publishFolder: {}'.format(publish_folder))

        msg = '.ass sequence already exists, use action to remove it first'
        assert not os.path.exists(publish_folder), msg
