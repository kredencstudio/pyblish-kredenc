import pyblish.api


@pyblish.api.log
class ExtractDeadlineHoudini(pyblish.api.Extractor):
    """ Gathers optional Draft related data for Deadline
    """
    order = pyblish.api.Extractor.order + 0.55
    families = ['deadline.render']
    hosts = ['houdini']
    version = (0, 1, 0)

    def process(self, instance):

        # getting job data
        job_data = {}
        if instance.has_data('deadlineJobData'):
            job_data = instance.data('deadlineJobData').copy()

        # setting optional data
        job_data['Pool'] = 'cg'
        job_data['ChunkSize'] = '1'
        # job_data['LimitGroups'] = 'houdini'

        group = 'hou'
        job_data['Group'] = group

        instance.set_data('deadlineJobData', value=job_data)
