import pyblish.api


@pyblish.api.log
class ExtractDeadlineDraftCustom(pyblish.api.Extractor):
    """ Gathers optional Draft related data for Deadline
    """
    order = pyblish.api.Extractor.order + 0.55
    families = ['deadline.render']
    hosts = ['nuke']
    version = (0, 1, 0)
    optional = True

    def process_context(self, context):

        # getting job data
        job_data = {}
        if context.has_data('deadlineJobData'):
            job_data = context.data('deadlineJobData').copy()

        # setting extra info key values
        extra_info_key_value = {}
        if 'ExtraInfoKeyValue' in job_data:
            extra_info_key_value = job_data['ExtraInfoKeyValue']

        t = r'K:\.core\repos\DeadlineRepository7\custom\draft\ftupload_encode_to_mov_h264_540p.py'
        extra_info_key_value['DraftTemplate'] = t
        extra_info_key_value['DraftUploadToFtrack'] = True

        context.set_data('deadlineJobData', value=job_data)
