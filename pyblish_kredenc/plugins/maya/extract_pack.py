import pyblish.api
import shutil
import os
import pyblish_maya
from maya import cmds
import pyblish_kredenc.utils as pyblish_utils
reload(pyblish_utils)

import subprocess


@pyblish.api.log
class ExtractPack(pyblish.api.Extractor):
    """Inject all models from the scene into the context"""

    families = ['pack']

    def process(self, instance):

        publish_path = instance.data['publishFile']

        if not os.path.exists(os.path.dirname(publish_path)):
            os.makedirs(os.path.dirname(publish_path))

        for f in instance.data['textures']:
            if os.path.isfile(f):
                new_tex = os.path.join(os.path.dirname(publish_path), os.path.basename(f))
                output = shutil.copy(f, new_tex)


        with pyblish_maya.maintained_selection():
            self.log.debug("instance: " + str(instance))
            cmds.select(instance)
            # preserveReferences = instance.data['preserveReferences'] or 'False'

            scene_name = os.path.basename(instance.context.data['currentFile'])

            dir_path = pyblish_utils.temp_dir(instance)
            new_scene = os.path.join(dir_path, scene_name)
            new_scene = os.path.join(new_scene).replace('\\', '/')
            self.log.debug('pack extraction path: {}'.format(new_scene))

            # new_scene = os.path.join(new_path, os.path.basename(instance.context.data['currentFile']))
            path = cmds.file(new_scene,
                             es=True,
                             constructionHistory=False,
                             preserveReferences=False,
                             shader=True,
                             channels=False,
                             constraints=False,
                             force=True,
                             type='mayaBinary')

            instance.data['outputPath'] = path

            script_path = r"K:\.core\dev\pyblish\pyblish-kredenc\pyblish_kredenc\utils\change_texture_fbx.py"

            command = r"mayapy {} {} {} & pause".format(script_path, new_scene, publish_path)

            subprocess.Popen(command)
