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

            name = rig.split('_')[0][1:]

            instance = context.create_instance(name=name, family="rig")

            instance.add(rig)

            # Add rig-specific object sets
            for objset in ("controls_set", "cache_set"):
                if cmds.objExists(objset):
                    instance.add(objset)

            instance.data["preserveReferences"] = False

            components = {}

            instance.data['ftrackComponents'] = components

            # instance.data['ftrackAssetName'] = name

            self.log.info("Successfully collected %s" % name)

            self.log.info("Successfully collected %s" % instance.data)
