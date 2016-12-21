import pyblish.api
import shutil

import os
import hou
import subprocess


@pyblish.api.log
class ExtractFlipbook(pyblish.api.Extractor):
    """Creates preview movie from a Flipbook bode"""

    families = ['review']
    hosts = ['houdini']
    version = (0, 1, 0)

    def process(self, instance):
        # submitting job

        preview = flip(instance[0])
        if os.path.isfile(preview):
            instance.data['outputPath_qt'] = preview
        else:
            raise pyblish.api.ValidationError('didn\'t create flipbook.')


def makeMovie(outputI, outputV, audio):
    if audio != '':
        audio = '-i ' + str(audio) + ' -map 0 -map 1 -c:a libtwolame'
    paddingExp = ".%4d"
    filename, extension = os.path.splitext(outputI)
    filename, padding = os.path.splitext(filename)
    input = filename + paddingExp + extension
    output = subprocess.call('ffmpeg -i {0} {2} -c:v libx264 -preset slow -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" -crf 19 -y {1}'.format(input, outputV, audio))
    return outputV



def flip(node):

    enable_prescript = node.parm('enable_prescript').eval()
    prescript = node.parm('prescript').eval()
    if enable_prescript:
        executeScript(prescript)

    cam = node.parm('cam').eval()
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
    width = node.parm('resx').eval()
    height = node.parm('resy').eval()

    import toolutils

    #Get the current Desktop
    desktop = hou.ui.curDesktop()

    # Get the scene viewer
    scene_view = desktop.createFloatingPaneTab(hou.paneTabType.SceneViewer, size=[1920,1080])

    #check of we are good to go
    if scene_view is None or scene_view.type() != hou.paneTabType.SceneViewer:
        raise hou.Error("No scene view available to playblast.")

    hou.hscript("viewcamera -c {0} *.*.world.persp1".format(cam))

    # Get the current viewport
    viewport = scene_view.curViewport()

    # Now build the name of the view required in the viewwrite command, this
    # is a little bit of magic, but is all procedural, except for the "world"
    # part...
    viewPane = desktop.name() + '.' + scene_view.name() + '.world'
    viewString =  viewPane + '.' + viewport.name()

    hou.hscript('vieweroption -V "-bone -null" {0}'.format(viewPane))

    try:
        os.makedirs(imagePath)
    except:
        pass

    cmd = ['viewwrite -r {0} {1}'.format(width, height)]
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
    cmd.append(viewString)
    cmd.append("'%s'"%outputIraw)

    i=0
    while not hou.hscript(' '.join(cmd))[0] == '':
        print 'waiting for vieport'
        i+=1
        if i == 10:
            return

    #close temporary viewport
    scene_view.close()

    print ' '.join(cmd)

    if enable_a:
        audio = node.parm('audio').eval()

    if enable_v:
        print 'video'
        makeMovie(outputI, outputV, audio)

    if enable_postscript:
        executeScript(postscript)

    if not enable_i:
        shutil.rmtree(imagePath)
