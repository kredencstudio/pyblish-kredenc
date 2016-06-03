import pyblish.api
import os


@pyblish.api.log
class ExtractDeadlineFFMPEG(pyblish.api.Extractor):
    """ Gathers Draft related data for Deadline
    """

    order = pyblish.api.Extractor.order + 0.4
    families = ['deadline.render']
    optional = True
    label = 'FFMPEG to Deadline'

    def process(self, instance):

        # getting job data
        job_data = {}
        if instance.has_data('deadlineData'):
            job_data = instance.data('deadlineData')['job'].copy()

        if 'ass.render' in instance.data['families']:
            return

        # setting extra info key values
        extra_info_key_value = {}
        if 'ExtraInfoKeyValue' in job_data:
            extra_info_key_value = job_data['ExtraInfoKeyValue']

        if '.exr' in job_data['OutputFilename0']:
            FFMPEGInputArgs = '-gamma 2.2 -framerate 25.0'
            FFMPEGOutputArgs = '-q:v 0 -pix_fmt yuv420p -vf scale=trunc(iw/2)*2:trunc(ih/2)*2,colormatrix=bt601:bt709'
        else:
            FFMPEGInputArgs = '-framerate 25.0'
            FFMPEGOutputArgs = '-q:v 0 -pix_fmt yuv420p -vf scale=trunc(iw/2)*2:trunc(ih/2)*2'

        output = os.path.splitext(os.path.splitext(job_data['OutputFilename0'])[0])[0]+'.mp4'

        extra_info_key_value['FFMPEGInputArgs0'] = FFMPEGInputArgs
        extra_info_key_value['FFMPEGOutputArgs0'] = FFMPEGOutputArgs
        extra_info_key_value['FFMPEGOutput0'] = output
        extra_info_key_value['FFMPEGUploadToFtrack'] = 'True'


        job_data['ExtraInfoKeyValue'] = extra_info_key_value

        data = instance.data('deadlineData')
        data['job'] = job_data
        instance.set_data('deadlineData', value=data)
