import pyblish.api
import os

import ftrack_api
from ftrack_kredenc import ft_utils


@pyblish.api.log
class IntegrateInitialScene(pyblish.api.Integrator):
    """Saves version one of the workfile
    """

    families = ['new_scene']
    hosts = ['nuke', 'maya', 'houdini']
    optional = True
    label = 'Initial Scene'
    order = pyblish.api.Integrator.order + 0.1

    def process(self, instance, context):

        if 'workfile' in instance.context.data:
            host = pyblish.api.current_host()
            workfile = instance.context.data['workfile']
            self.log.info("workfile '%s'" % workfile)

            if host == 'nuke':
                import nuke
                nuke.scriptSaveAs(workfile)
            elif host == 'maya':
                import pymel.core as pm
                if os.path.exists(workfile):
                    pm.system.openFile(workfile, force=True)
                else:

                    if context.data['ftrackData']['Project']['code'] == 'hbt':
                        from ftrack_kredenc import ft_maya
                        reload(ft_maya)
                        import maya_utils as mu
                        reload(mu)
                        try:
                            if (context.data['ftrackData']['Task']['code']).lower() in ['anim', 'animation', 'render', 'layout', 'lighting', 'light']:
                                shotId = os.getenv('FTRACK_SHOTID')
                                session = ftrack_api.Session()
                                shot = session.query('Shot where id is {}'.format(shotId)).one()
                                handles = int(shot['custom_attributes']['handles'])
                                sf = int(shot['custom_attributes']['fstart'])
                                ef = int(shot['custom_attributes']['fend'])

                                ft_maya.framerate_init()
                                pm.playbackOptions(playbackSpeed = 1.0)
                                pm.playbackOptions(ast=sf-handles, aet=ef+handles, min=sf-handles, max=ef+handles)
                                #change path by hand
                                publishArr = workfile.split('\\')
                                del publishArr[-1]
                                del publishArr[-1]
                                del publishArr[-1]
                                newPath = ("/".join(publishArr)) + "/publish/audio"
                                mu.loadSound(newPath, sf = (sf-handles), fileTypes = ['wav'])
                        except:
                            pass
                        import hbt_renderSetup
                        reload(hbt_renderSetup)
                        hbt_renderSetup.run()

                    pm.saveAs(workfile, type='mayaAscii')
                    #load sound if hbt project and has sound

                proj_path = os.path.dirname(workfile)
                self.log.info("Setting Maya project to '%s'" % proj_path)
                pm.mel.setProject(proj_path)
            elif host == 'houdini':
                import hou
                if os.path.exists(workfile):
                    hou.hipFile.open(hou.expandString(workfile).replace('\\', '/'))
                else:
                    hou.hipFile.save(hou.expandString(workfile).replace('\\', '/'))

        else:
            raise pyblish.api.ValidationError(
                "Can't find workfile in instance.context.")
