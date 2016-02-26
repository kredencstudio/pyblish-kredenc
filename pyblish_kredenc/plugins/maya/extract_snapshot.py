import os
import contextlib

import pyblish.api
from pyblish_kredenc.vendor import capture

from maya import cmds
import pymel.core as pm


@pyblish.api.log
class ExtractSnapshot(pyblish.api.Extractor):
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
    label = "Snapshot"

    def process(self, instance):
        self.log.info("Extracting capture..")
        components = instance.data['ftrackComponents'].copy()
        self.log.debug('Components: {}'.format(components))

        format = instance.data('format') or 'image'
        # # compression = instance.data('compression') or 'h264'
        off_screen = instance.data('offScreen', False)
        maintain_aspect_ratio = instance.data('maintainAspectRatio', True)

        camera = instance[0]

        try:
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

        except:
            camera_shape = cmds.listRelatives(camera, shapes=True)[0]

            preset = {
                "camera": camera,
                "width": cmds.getAttr("defaultResolution.width"),
                "height": cmds.getAttr("defaultResolution.height"),
                "camera_options": type("CameraOptions", (object, capture.CameraOptions,), {
                    "displayFilmGate": cmds.getAttr(camera_shape + ".displayFilmGate"),
                    "displayResolution": cmds.getAttr(camera_shape + ".displayResolution"),
                    "displaySafeAction": cmds.getAttr(camera_shape + ".displaySafeAction"),
                }),
                "viewport_options": type("ViewportOptions", (object, capture.ViewportOptions,), {
                    "useDefaultMaterial": False,
                    # "wireframeOnShaded": cmds.modelEditor(panel, query=True, wireframeOnShaded=True),
                    # "displayAppearance": cmds.modelEditor(panel, query=True, displayAppearance=True),
                    # "displayTextures": cmds.modelEditor(panel, query=True, displayTextures=True),
                    # "displayLights": cmds.modelEditor(panel, query=True, displayLights=True),
                    # "shadows": cmds.modelEditor(panel, query=True, shadows=True),
                    # "xray": cmds.modelEditor(panel, query=True, xray=True),
                }),
                "display_options": type("DisplayOptions", (object, capture.DisplayOptions,), {
                    "background": cmds.displayRGBColor('background', q=True),
                    "backgroundTop": cmds.displayRGBColor('backgroundTop', q=True),
                    "backgroundBottom": cmds.displayRGBColor('backgroundBottom', q=True),
                    'displayGradient': cmds.displayPref(dgr=True, q=True),
                }),
            }


        # Ensure name of camera is valid
        sourcePath = os.path.normpath(instance.context.data('currentFile'))
        path, extension = os.path.splitext(sourcePath)
        path = (path + ".jpg")


        self.log.info("preset %s" % preset['viewport_options'].polymeshes)

        self.log.info("Outputting to %s" % path)

        with maintained_time():
            output = capture.snap(
                # camera=camera,
                # width=width,
                # height=height,
                filename=path,
                format=format,
                viewer=False,
                off_screen=off_screen,
                maintain_aspect_ratio=maintain_aspect_ratio,
                overwrite=True,
                quality=50,
                **preset
                )


        instance.data["outputPath_jpg"] = output


@contextlib.contextmanager
def maintained_time():
    ct = cmds.currentTime(query=True)
    try:
        yield
    finally:
        cmds.currentTime(ct, edit=True)
