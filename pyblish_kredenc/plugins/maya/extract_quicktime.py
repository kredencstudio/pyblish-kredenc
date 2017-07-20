import os
import contextlib

import pyblish.api
import capture_gui

import pyblish_kredenc.utils as pyblish_utils

from maya import cmds


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
                          '_cam' suffix")
            return

        # PROJECT FILTERING

        project_code = instance.context.data['ftrackData']['Project']['code']
        task_type = instance.context.data['ftrackData']['Task']['type']

        # load Preset
        studio_repos = os.path.abspath(os.environ.get('studio_repos'))
        task_preset_path = os.path.join(studio_repos, 'maya',
                                    'capture_gui_presets',
                                   (project_code + '_' + task_type + '.json'))

        project_preset_path = os.path.join(studio_repos, 'maya',
                                   'capture_gui_presets',
                                   (project_code + '.json'))

        default_preset_path = os.path.join(studio_repos, 'maya',
                                   'capture_gui_presets',
                                   'default.json')


        # my_file = Path("/path/to/file")
        if os.path.isfile(task_preset_path):
            preset_to_use = task_preset_path
        elif os.path.isfile(project_preset_path):
            preset_to_use = project_preset_path
        else:
            preset_to_use = default_preset_path

        preset = pyblish_utils.load_capture_preset(preset_to_use)
        self.log.info('using viewport preset: {}'.format(preset_to_use))


        preset['camera'] = camera
        preset['compression'] = "H.264"

        dir_path = pyblish_utils.temp_dir(instance)

        # Ensure name of camera is valid
        sourcePath = os.path.normpath(instance.context.data('currentFile'))
        path, extension = os.path.splitext(sourcePath)
        image_folder, filename = os.path.split(path)
        output_images = os.path.join(dir_path, filename)

        self.log.info("Outputting images to %s" % output_images)

        # CLEAR HUDS

        huds = cmds.headsUpDisplay(lh=True)
        stored_huds = []
        for hud in huds:
            if cmds.headsUpDisplay(hud, vis=True, q=True):
                stored_huds.append(hud)
                cmds.headsUpDisplay(hud, vis=False, e=True)

        # Export Playblast

        preset['filename'] = output_images
        preset['overwrite'] = True

        with maintained_time():
            playblast = capture_gui.lib.capture_scene(preset)

        instance.data["outputPath_qt"] = playblast
        self.log.info("Outputting video to %s" % playblast)

        for hud in stored_huds:
            cmds.headsUpDisplay(hud, vis=True, e=True)


@contextlib.contextmanager
def maintained_time():
    ct = cmds.currentTime(query=True)
    try:
        yield
    finally:
        cmds.currentTime(ct, edit=True)
