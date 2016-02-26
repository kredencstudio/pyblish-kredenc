import pyblish.api

import maya.cmds as cmds

@pyblish.api.log
class CollectCameras(pyblish.api.Collector):

    order = pyblish.api.Collector.order + 0.2
    hosts = ["maya"]
    label = "Collect Cameras"

    def process(self, context):
        for camera_shape in cmds.ls("*_cam*",
                                    objectsOnly=True,
                                    type="camera",
                                    long=True,
                                    recursive=True):  # Include namespace

            camera = cmds.listRelatives(camera_shape, parent=True)[0]

            # Use short name
            name = cmds.ls(camera, long=False)[0].lower()

            instance = context.create_instance(name=name, family='camera')
            instance.add(camera)
            instance.data["publish"] = False

            attrs = cmds.listAttr(camera, userDefined=True) or list()

            self.log.info("Found: %s" % camera)
            self.log.info("Overrides: %s" % attrs)

            for attr in attrs:
                try:
                    value = cmds.getAttr(camera + "." + attr)
                except:
                    self.log.warning("Could not read from: %s" % attr)
                    continue

                self.log.debug("Adding %s=%s to %s" % (
                    attr, value, instance))

                instance.data[attr] = value

            # ftrack data
            components = {'ma': {'path': ''}}

            instance.data['ftrackComponents'] = components
            self.log.info("Added: %s" % components)
