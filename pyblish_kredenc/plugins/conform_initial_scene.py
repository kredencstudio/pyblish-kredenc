import pyblish.api
import nuke

@pyblish.api.log
class IntegrateInitialScene(pyblish.api.Integrator):
    """Saves version one of the workfile
    """

    families = ['new_scene']
    hosts = ['nuke']
    optional = True
    label = 'Initial Scene'

    def process(self, context, instance):

        if 'workfile' in context.data:

            workfile = context.data['workfile']
            nuke.scriptSaveAs(workfile)

        else:
            raise pyblish.api.ValidationError(
                "Can't find workfile in context.")
