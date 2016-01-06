import pyblish.api
import os


@pyblish.api.log
class IntegrateInitialScene(pyblish.api.Integrator):
    """Saves version one of the workfile
    """

    families = ['new_scene']
    hosts = ['nuke', 'maya']
    optional = True
    label = 'Initial Scene'

    def process(self, context, instance):

        if 'workfile' in context.data:
            host = pyblish.api.current_host()
            workfile = context.data['workfile']
            self.log.info("workfile '%s'" % workfile)

            if host == 'nuke':
                import nuke
                nuke.scriptSaveAs(workfile)
            elif host == 'maya':
                import pymel.core as pm
                if os.path.exists(workfile):
                    pm.system.openFile(workfile, force=True)
                else:
                    pm.saveAs(workfile, type='mayaAscii')

                proj_path = os.path.dirname(workfile)
                self.log.info("Setting Maya project to '%s'" % proj_path)
                pm.mel.setProject(proj_path)

        else:
            raise pyblish.api.ValidationError(
                "Can't find workfile in context.")
