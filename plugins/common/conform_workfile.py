import pyblish.api
import sys

@pyblish.api.log
class VersionUpWorkfile(pyblish.api.Conformer):
    """Versions up current workfile"""

    families = ['workFile']
    hosts = ['*']
    version = (0, 1, 0)
    optional = True
    host = sys.executable.lower()

    def process_instance(self, instance):

        if instance.has_data('new_workfile'):
            new_workfile = instance.context.data('new_workfile')
            if "nuke" in self.host:
                self.process_nuke(new_workfile)
            elif "maya" in self.host:
                self.process_maya(new_workfile)
            elif "houdini" in self.host:
                self.process_houdini(new_workfile)
        else:
            self.log.warning("Can't find versioned up filename in context."
                             "workfile probably doesn't have a version.")

    # NUKE
    def process_nuke(self, new_workfile):
        import nuke
        nuke.scriptSaveAs(new_workfile)

    # MAYA
    def process_maya(self, new_workfile):
        import cmds
        cmds.file(save=True, rename=new_workfile)

    # HOUDINI
    def process_houdini(self, new_workfile):
        import hou
        hou.hipFile.save(file_name=new_workfile)
