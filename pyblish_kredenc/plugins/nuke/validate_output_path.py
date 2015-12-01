import os
import pyblish.api


@pyblish.api.log
class ValidateOutputPath(pyblish.api.Validator):
    """Validates that the output directory for the instance exists"""

    families = ['writeNode', 'prerenders']
    hosts = ['nuke']
    version = (0, 1, 0)

    def process(self, instance):
        name = instance[0].name()

        try:
            path = os.path.dirname(instance[0]['file'].value())
        except:
            path = None

        if path:
            if not os.path.exists(path):
                msg = 'Output directory for %s doesn\'t exists' % name
                self.log.error(msg)
                raise pyblish.api.ValidationError('You can run repair to create the directory automatically'
                                                  'or create it manually and re-run the publish')
        else:
            raise pyblish.api.ValidationError('No output directory could be found in %s, hence it can\'t be validated' % name)


    def repair(self, instance):
        """Auto-repair creates the output directory"""
        path = os.path.dirname(instance[0]['file'].value())

        if not os.path.exists(path):
            os.makedirs(path)
