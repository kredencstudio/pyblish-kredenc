import pyblish.api
import shutil

import os
import shutil
import hou
import subprocess


@pyblish.api.log
class ExtractFlipbook(pyblish.api.Extractor):
    """Creates preview movie from a Flipbook bode"""

    families = ['preview']
    hosts = ['houdini']
    version = (0, 1, 0)
    optional = True

    def process_instance(self, instance):
        # submitting job

        preview = flip(instance[0])
        print preview
        if os.path.isfile(preview):
            instance.set_data('output_path', value=preview)
        else:
            raise pyblish.api.ValidationError('didn\'t create flipbook.')


def makeMovie(outputI, outputV, audio):
    if audio != '':
        audio = '-i ' + audio + ' -map 0 -map 1 -c:a libtwolame'
    paddingExp = ".%4d"
    file, extension = os.path.splitext(outputI)
    file, padding = os.path.splitext(file)
    input = file + paddingExp + extension
    output = subprocess.call('ffmpeg -i {0} {2} -b:v 2000k -c:v h264 -pix_fmt yuv420p -preset slow -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" -y {1}'.format(input, outputV, audio))
    return outputV

def flip(node):

    enable_prescript = node.parm('enable_prescript').eval()
    prescript = node.parm('prescript').eval()
    if enable_prescript:
        executeScript(prescript)

    enable_postscript = node.parm('enable_postscript').eval()
    postscript = node.parm('postscript').eval()
    outputIraw = node.parm('output').unexpandedString()
    outputI = node.parm('output').eval()
    audio = ''
    imagePath, imageFile = os.path.split(outputI)
    outputV = node.parm('outputV').eval()
    startf = node.parm('f1').eval()
    endf = node.parm('f2').eval()
    incf = node.parm('f3').eval()
    enable_v = node.parm('enable_v').eval()
    enable_a = node.parm('enable_a').eval()
    enable_i = node.parm('enable_i').eval()
    enable_b = node.parm('enable_b').eval()
    b = node.parm('b').eval()
    enable_g = node.parm('enable_g').eval()
    g = node.parm('g').eval()
    v = node.parm('v').eval()
    B = node.parm('B').eval()
    I = node.parm('I').eval()
    c = node.parm('c').eval()

    import toolutils

    #Get the current Desktop
    desktop = hou.ui.curDesktop()

    # Get the scene viewer
    scene_view = toolutils.sceneViewer()

    #check of we are good to go
    if scene_view is None or scene_view.type() != hou.paneTabType.SceneViewer:
        raise hou.Error("No scene view available to playblast.")

    # Get the current viewport
    viewport = scene_view.curViewport()

    # Now build the name of the view required in the viewwrite command, this
    # is a little bit of magic, but is all procedural, except for the "world"
    # part...
    view = desktop.name() + '.' + scene_view.name() + '.world.' + viewport.name()


    #view = '%s.%s.%s.%s' %(desktop.name(), pane.name(), 'world', viewPort.name())

    try:
        os.makedirs(imagePath)
    except:
        pass

    cmd = ['viewwrite']
    cmd.append('-f')
    cmd.append(str(startf))
    cmd.append(str(endf))
    cmd.append('-i')
    cmd.append(str(incf))
    if enable_b:
        cmd.append('-b')
        cmd.append("'%s'"%b)
    if enable_g:
        cmd.append('-g')
        cmd.append(str(g))
    cmd.append('-v')
    cmd.append('"%s"'%v)
    if B:
        cmd.append('-B')
    if I:
        cmd.append('-I')
    if c:
        cmd.append('-c')
    cmd.append(view)
    cmd.append("'%s'"%outputIraw)


    hou.hscript(' '.join(cmd))

    print ' '.join(cmd)

    if enable_a:
        audio = node.parm('audio').eval()

    if enable_v:
        print 'video'
        return makeMovie(outputI, outputV, audio)

    if enable_postscript:
        executeScript(postscript)

    if not enable_i:
        shutil.rmtree(imagePath)
