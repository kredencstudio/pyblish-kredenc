import pyblish.api
import os
import sys
import pprint

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pyblish_utils

@pyblish.api.log
class SelectWorkfile(pyblish.api.Selector):
    """Selects current workfile"""

    hosts = ['*']
    version = (0, 1, 0)

    host = sys.executable.lower()

    def process_context(self, context):
        if "nuke" in self.host:
            current_file = self.process_nuke()
            current_file = os.path.normpath(current_file)
        elif "maya" in self.host:
            current_file = self.process_houdini()
        elif "houdini" in self.host:
            current_file = self.process_houdini()
        else:
            current_file = None
            self.log.warning('Workfile selection in current host is not supported yet!')

        directory, filename = os.path.split(current_file)
        try:
            (prefix, version) = pyblish_utils.version_get(filename, 'v')
        except:
            self.log.warning('Cannot publish workfile which is not versioned.')
            return

        if current_file:
            context.set_data('currentFile', value=current_file)
            context.set_data('version', value=version)
            context.set_data('vprefix', value=prefix)
            instance = context.create_instance(name=filename)
            instance.set_data('family', value='workFile')
            instance.set_data("path", value=current_file)
            instance.add(current_file)


    # NUKE
    def process_nuke(self):
        import nuke
        return nuke.root().name()

    # MAYA
    def process_maya(self):
        import cmds
        return cmds.file(q=True, location=True)

    # HOUDINI
    def process_houdini(self):
        import hou
        return hou.hipFile.path()
