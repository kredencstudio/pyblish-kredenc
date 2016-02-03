import os
import instance.contextlib

import pyblish.api
from pyblish_kredenc.vendor import capture

from maya import cmds
import pymel.core as pm


@pyblish.api.log
class ExtractQuicktime(pyblish.api.Extractor):
    """Extract review instances as a quicktime

    Arguments:
        startFrame (float): Start frame of output
        endFrame (float): End frame of output
        width (int): Width of output in pixels
        height (int): Height of output in pixels
        format (str): Which format to use for the given filename,
            defaults to "qt"
        compression (str): Which compression to use with the given
            format, defaults to "h264"
        offScreen (bool): Capture off-screen
        maintainAspectRatio (bool): Whether or not to modify height for width
            in order to preserve the current aspect ratio.
        show (str): Space-separated list of which node-types to show,
            e.g. "nurbsCurves polymeshes"

    """

    families = ["review"]
    hosts = ["maya"]
    optional = True
    label = "Quicktime"

    def process(self, instance):
        self.log.info("Extracting capture..")
        components = instance.data['ftrackComponents'].copy()
        self.log.debug('Components: {}'.format(components))

        camera = instance[0]

        current_min_time = cmds.playbackOptions(minTime=True, query=True)
        current_max_time = cmds.playbackOptions(maxTime=True, query=True)

        default_width = cmds.getAttr("defaultResolution.width")
        default_height = cmds.getAttr("defaultResolution.height")

        width = instance.data('width') or default_width
        height = instance.data('height') or default_height
        start_frame = instance.data('startFrame') or current_min_time
        end_frame = instance.data('endFrame') or current_max_time

        format = instance.data('format') or 'qt'
        compression = instance.data('compression') or 'h264'
        off_screen = instance.data('offScreen', False)
        maintain_aspect_ratio = instance.data('maintainAspectRatio', True)

        cam_opts = capture.CameraOptions()

        # Set viewport settings
        view_opts = capture.ViewportOptions()
        view_opts.displayAppearance = "smoothShaded"
        view_opts.dtx = True
        view_opts.grid = False

        # Set display settings

        display_options = capture.DisplayOptions()
        display_options.background = pm.displayRGBColor('background', q=True)
        display_options.backgroundTop = pm.displayRGBColor('backgroundTop', q=True)
        display_options.backgroundBottom = pm.displayRGBColor('backgroundBottom', q=True)
        display_options.displayGradient = pm.displayPref(dgr=True, q=True)


        if 'show' in instance.data():
            for nodetype in instance.data('show').split():
                self.log.info("Overriding show: %s" % nodetype)
                if hasattr(view_opts, nodetype):
                    setattr(view_opts, nodetype, True)
                else:
                    self.log.warning("Specified node-type in 'show' not "
                                     "recognised: %s" % nodetype)
        else:
            view_opts.polymeshes = True
            view_opts.nurbsSurfaces = True


        # Ensure name of camera is valid
        sourcePath = os.path.normpath(instance.context.data('currentFile'))
        path, extension = os.path.splitext(sourcePath)


        if format == 'image':
            # Append sub-directory for image-sequence
            path = os.path.join(path, camera)
        else:
            path = (path + ".mov")

        self.log.info("Outputting to %s" % path)

        with maintained_time():
            output = capture.capture(
                camera=camera,
                width=width,
                height=height,
                filename=path,
                start_frame=start_frame,
                end_frame=end_frame,
                format=format,
                viewer=False,
                compression=compression,
                off_screen=off_screen,
                maintain_aspect_ratio=maintain_aspect_ratio,
                viewport_options=view_opts,
                camera_options=cam_opts,
                overwrite=True,
                quality=50,
                display_options=display_options,
                )



        instance.data["outputPath"] = output


@instance.contextlib.instance.contextmanager
def maintained_time():
    ct = cmds.currentTime(query=True)
    try:
        yield
    finally:
        cmds.currentTime(ct, edit=True)
