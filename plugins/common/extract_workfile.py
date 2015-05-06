import pyblish.api
import shutil
import sys
# import nuke

@pyblish.api.log
class publishWorkfile(pyblish.api.Extractor):
    """Publishes current workfile to a _Publish location, next to current working directory"""

    # order = pyblish.api.Extractor.order + 0.1
    families = ['workFile']
    hosts = ['*']
    version = (0, 1, 0)
    # optional = True
    host = sys.executable.lower()

    def process_instance(self, instance):
        # submitting job
        sourcePath = instance.data('path')
        new_workfile = instance.context.data('new_workfile')
        publishPath = instance.context.data('published_scene_file')

        print publishPath

        shutil.copy(sourcePath, publishPath)

        if "nuke" in self.host:
            self.process_nuke(new_workfile)
        elif "maya" in self.host:
            self.process_maya(new_workfile)
        elif "houdini" in self.host:
            print 'TO SAVE' + new_workfile
            self.process_houdini(new_workfile)

    # NUKE
    def process_nuke(self, new_workfile):
        import nuke
        nuke.scriptSaveAs(new_workfile)

    # MAYA
    def process_maya(self, new_workfile):
        pass
        import cmds
        # return cmds.file(q=True, location=True)

    # HOUDINI
    def process_houdini(self, new_workfile):
        import hou
        return hou.hipFile.save(file_name=new_workfile)
