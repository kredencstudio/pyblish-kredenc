import os
import pyblish.api
import pymel
import pyblish_maya


@pyblish.api.log
class CollectRig(pyblish.api.Collector):
    """Inject all rigs from the scene into the context"""

    hosts = ["maya"]

    def process(self, context):
        from maya import cmds

        for rig in cmds.ls( "*rig_grp*",
                            objectsOnly=True,
                            type="transform",
                            long=True,
                            recursive=True):

            # Get the root transform
            self.log.info("Rig found: {}".format(str(rig)))
            assembly = rig

            name = os.environ['asset_build_name']

            assert cmds.objExists(assembly), (
                "Rig did not have an appropriate assembly: %s" % assembly)

            instance = context.create_instance(name=name, family="rig")

            # # Add rig-specific object sets
            # for objset in ("controls_SET", "pointcache_SET"):
            #     if cmds.objExists(objset):
            #         instance.add(objset)

            instance.set_data("preserveReferences", False)

            components = {'mayaAscii': {'path': ''}}
            
            instance.data['ftrackComponents'] = components

            self.log.info("Successfully collected %s" % name)
