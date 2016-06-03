import pyblish.api


@pyblish.api.log
class ExtractDeadlineDraftCustom(pyblish.api.Extractor):
    """ Gathers optional Nuke related data for Deadline
    """
    order = pyblish.api.Extractor.order + 0.49
    families = ['deadline.render']
    hosts = ['nuke']
    optional = True

    def process(self, instance):


        # getting job data
        job_data = {}
        if instance.has_data('deadlineData'):
            job_data = instance.data['deadlineData']['job'].copy()

        # setting extra info key values
        extra_info_key_value = {}
        if 'ExtraInfoKeyValue' in job_data:
            extra_info_key_value = job_data['ExtraInfoKeyValue']


        t = r'K:\.core\repos\DeadlineRepository7\custom\draft\ftupload_encode_to_mov_h264_720p.py'
        extra_info_key_value['DraftTemplate'] = t
        extra_info_key_value['DraftUploadToFtrack'] = True

        instance.data['deadlineData']['job'] = job_data
