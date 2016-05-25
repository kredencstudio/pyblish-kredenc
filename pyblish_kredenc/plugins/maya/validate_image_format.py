import os

import pyblish.api


@pyblish.api.log
class ValidateImageFormat(pyblish.api.Validator):
    """ Validates settings """
    hosts = ['maya']
    families = ['render']
    optional = True
    label = 'Image Format'

    def process(self, instance):

        ext = os.path.splitext(instance.data('deadlineData')['job']['OutputFilename0'])[1]

        msg = 'Image format is incorrect. Needs to be either EXR or PNG'
        assert ext in ['.exr', '.png'], msg
