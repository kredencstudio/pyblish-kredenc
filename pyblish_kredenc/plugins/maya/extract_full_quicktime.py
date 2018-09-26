import os
import contextlib
import time

import pyblish.api
import capture_gui

import pyblish_kredenc.utils as pyblish_utils

from maya import cmds
import pymel.core as pm

import maya_utils as mu
reload(mu)

from tweakHUD import master
reload(master)

from tweakHUD import draft_hud as dHUD
reload(dHUD)

from tweakHUD import ftrackStrings as fStrings
reload(fStrings)


@pyblish.api.log
class ExtractFullQuicktime(pyblish.api.Extractor):
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
    label = "Full Quicktime"
    active = True

    def process(self, instance):

        def temp_dir():
            import tempfile
            extract_dir = tempfile.mkdtemp()
            return extract_dir



        self.log.info("Extracting full capture..")
        #ftrackData = context.data.get('ftrackData')

        if instance.context.data.get('ftrackData'):
            if instance.context.data['ftrackData']['Project']['code'] == 'hbt':
                self.log.info("Switching texures to LOW")
                import hbt_switch_tex as hbtSw
                reload(hbtSw)

                nhbtData=hbtSw.switchTexture()

                nhbtData.option = 1
                nhbtData.highest = False
                nhbtData.limit = 1600
                nhbtData.validatorCheck()
                nhbtData.fast = False

                nhbtData.all = True
                nhbtData.forceReload = True
                nhbtData.switch()

                pm.refresh(f=True)


        components = instance.data['ftrackComponents'].copy()
        self.log.debug('Components: {}'.format(components))

        camera = instance[0]

        if 'persp' in camera:
            self.log.info("If you want movie review, create a camera with \
                          '_cam' suffix")
            return


        ftrack_data = instance.context.data['ftrackData']

        project_code = ftrack_data['Project']['code']
        task_type = ftrack_data['Task']['type']

        if 'Asset_Build' in ftrack_data:
            asset = ftrack_data['Asset_Build']['name']
        elif 'Shot' in ftrack_data:
            asset = ftrack_data['Shot']['name']


        ftrackStrings = fStrings.annotationData()
        nData = ftrackStrings.niceData
        nData['version'] = instance.context.data('version')

        fFrame = int(float(nData['oFStart']))
        eFrame = int(float(nData['oFEnd']))
        fHandle = int(float(nData['handle']))
        soundOfst = 0 #fFrame - fHandle - fFrame
        nData['frame'] = [(str("{0:05d}".format(f))) for f in range(fFrame - fHandle, eFrame + fHandle + 1)]



        # load Preset
        studio_repos = os.path.abspath(os.environ.get('studio_repos'))
        shot_preset_path = os.path.join(studio_repos, 'maya',
                                    'capture_gui_presets',
                                   (project_code + '_' + task_type + '_' + asset + '.json'))

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
        if os.path.isfile(shot_preset_path):
            preset_to_use = shot_preset_path
        elif os.path.isfile(task_preset_path):
            preset_to_use = task_preset_path
        elif os.path.isfile(project_preset_path):
            preset_to_use = project_preset_path
        else:
            preset_to_use = default_preset_path

        preset = pyblish_utils.load_capture_preset(preset_to_use)
        self.log.info('using viewport preset: {}'.format(preset_to_use))


        #preset["off_screen"] =  False

        preset['camera'] = camera
        preset['format'] = "image"
        preset['compression'] = "jpg"
        preset['quality'] = 95
        #preset['compression'] = "H.264"
        preset['camera_options'] = {
            "displayGateMask": False,
            "displayResolution": False,
            "displayFilmGate": False,
            "displayFieldChart": False,
            "displaySafeAction": False,
            "displaySafeTitle": False,
            "displayFilmPivot": False,
            "displayFilmOrigin": False,
            "overscan": 1.0,
            "depthOfField": cmds.getAttr("{0}.depthOfField".format(camera))
        }

        dir_path = temp_dir()

        # Ensure name of camera is valid
        sourcePath = os.path.normpath(instance.context.data('currentFile'))
        path, extension = os.path.splitext(sourcePath)
        image_folder, filename = os.path.split(path)
        output_images = os.path.join(dir_path, filename)

        self.log.info("Outputting images to %s" % output_images)


        preset['filename'] = output_images
        preset['overwrite'] = True


        preset['start_frame'] = fFrame - fHandle
        preset['end_frame'] = eFrame + fHandle

        pm.refresh(f=True)


        refreshFrameInt = fFrame - fHandle
        pm.currentTime( refreshFrameInt - 1, edit=True )
        pm.currentTime( refreshFrameInt, edit=True )

        with maintained_time():
            playblast = capture_gui.lib.capture_scene(preset)


        self.log.info("Calculating HUD data overlay")

        movieFullPth = output_images + ".mov"
        #wildCardMoviePth = output_images + ".*"
        fls = [os.path.join(dir_path, f).replace("\\","/") for f in os.listdir( dir_path ) if f.endswith(preset['compression'])]
        #self.log.info(" these  %s" % fls[0])



        soundFile = mu.giveMePublishedAudio()
        self.log.info("SOUND offset  %s" % str(soundOfst))
        self.log.info("SOUND source video to %s" % str(soundFile))
        ann = dHUD.draftAnnotate()
        if soundFile:
            ann.addAnotation(seqFls = fls, outputMoviePth = movieFullPth, annotateDataArr = nData, soundFile = soundFile, soundOffset = soundOfst)
        else:
            ann.addAnotation(seqFls = fls, outputMoviePth = movieFullPth, annotateDataArr = nData)


        for f in fls:
            os.remove(f)

        playblast = (ann.expPth).replace("\\","/")
        instance.data["handleOutputPath_qt"] = movieFullPth
        self.log.info("Outputting full video to %s" % movieFullPth)

        #instance.data['ftrackComponents']['fullReview'] = {'path': "", 'reviewable': False}


@contextlib.contextmanager
def maintained_time():
    ct = cmds.currentTime(query=True)
    try:
        yield
    finally:
        cmds.currentTime(ct, edit=True)
