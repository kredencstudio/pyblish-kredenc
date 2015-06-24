import os
import pyblish.api


@pyblish.api.log
class ValidateFlipbookAudio(pyblish.api.Validator):
    """Validates that the output directory for the instance exists"""

    families = ['preview']
    hosts = ['houdini']
    version = (0, 1, 0)

    def process(self, instance):
        name = instance[0].name()
        audio = instance[0].parm('audio').eval()
        enable_a = instance[0].parm('enable_a').eval()

        if enable_a:
            if audio == '':
                msg = '%s audio is empty. Preview will be created without sound' % name
                raise pyblish.api.ValidationError(msg)
            else:
                if not os.path.isfile(audio):
                    raise pyblish.api.ValidationError('audio: %s, could not be found' % audio)



    #
    # def repair_instance(self, instance):
    #     """Auto-repair creates the output directory"""
    #     path = os.path.dirname(instance[0]['file'].value())
    #
    #     if not os.path.exists(path):
    #         os.makedirs(path)
