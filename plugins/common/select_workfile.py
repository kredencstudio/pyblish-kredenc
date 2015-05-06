import pyblish.api
import os

@pyblish.api.log
class SelectWorkfile(pyblish.api.Selector):
    """Selects current workfile"""

    hosts = ['*']
    version = (0, 1, 0)

    def process_context(self, context):

        if "nuke" in sys.executable:
            current_file = self.process_nuke()
        elif "maya" in sys.executable:
            current_file = self.process_houdini()
        elif "houdini" in sys.executable:
            current_file = self.process_houdini()
        else:
            current_file = True

        # Normalise the path
        normalised = os.path.normpath(current_file)

        directory, filename = os.path.split(normalised)

        instance = context.create_instance(name=filename)
        instance.set_data('family', value='workFile')
        # instance.set_data("publish", False)
        instance.set_data("path", value=normalised)
        instance.add(normalised)


    # NUKE
    def process_nuke(self):
        import nuke
        return nuke.root().name()

    # MAYA
    def process_maya(self):
        import cmds
        return cmds.file(q=True, modified=True)

    # HOUDINI
    def process_houdini(self):
        import hou
        return hou.hipFile.path()()
