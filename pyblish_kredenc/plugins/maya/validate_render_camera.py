import pymel
import pyblish.api


@pyblish.api.log
class ValidateRenderCamera(pyblish.api.Validator):
    """ Validates settings """
    hosts = ['maya']
    families = ['deadline.render']
    optional = True
    label = 'Render Camera'

    def process(self, instance):

        # validate non native camera active
        render_cameras = []
        for c in pymel.core.ls(type='camera'):
            if c.renderable.get():
                render_cameras.append(c)

        msg = 'No renderable camera selected.'
        assert render_cameras, msg

        check = True
        for c in render_cameras:
            if c.getParent().name() in ['persp', 'top', 'side', 'front']:
                check = False

        msg = 'Renderable Cameras is incorrect. Expected non default camera.'
        assert check, msg
