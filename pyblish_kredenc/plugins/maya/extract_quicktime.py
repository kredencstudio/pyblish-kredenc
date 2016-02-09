import os
import contextlib

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

        if 'persp' in camera:
            self.log.info("If you want movie review, create a camera with \
                          '_CAM' suffix")
            return

        format = instance.data('format') or 'qt'
        compression = instance.data('compression') or 'h264'
        off_screen = instance.data('offScreen', False)
        maintain_aspect_ratio = instance.data('maintainAspectRatio', True)


        preset = capture.parse_active_view()

        if 'show' in instance.data():
            self.log.info("Overriding show: %s" % instance.data['show'])
            for nodetype in instance.data['show']:
                # self.log.info("Overriding show: %s" % nodetype)
                if hasattr(preset['viewport_options'], nodetype):
                    setattr(preset['viewport_options'], nodetype, True)
                else:
                    self.log.warning("Specified node-type in 'show' not "
                                     "recognised: %s" % nodetype)


        # Ensure name of camera is valid
        sourcePath = os.path.normpath(instance.context.data('currentFile'))
        path, extension = os.path.splitext(sourcePath)
        path = (path + ".png")

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
                # camera=camera,
                # width=width,
                # height=height,
                filename=path,
                # start_frame=start_frame,
                # end_frame=end_frame,
                format=format,
                viewer=False,
                compression=compression,
                off_screen=off_screen,
                maintain_aspect_ratio=maintain_aspect_ratio,
                overwrite=True,
                quality=50,
                **preset
                )


        instance.data["outputPath_qt"] = output


@contextlib.contextmanager
def maintained_time():
    ct = cmds.currentTime(query=True)
    try:
        yield
    finally:
        cmds.currentTime(ct, edit=True)
