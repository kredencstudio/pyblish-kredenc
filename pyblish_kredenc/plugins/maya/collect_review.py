import pyblish.api

import maya.cmds as cmds


@pyblish.api.log
class CollectCameras(pyblish.api.Collector):
    order = pyblish.api.Collector.order + 0.2
    hosts = ["maya"]
    label = "Collect Cameras"

    def process(self, context):
        for camera_shape in cmds.ls("*_CAM*",
                                    objectsOnly=True,
                                    type="camera",
                                    long=True,
                                    recursive=True):  # Include namespace

            camera = cmds.listRelatives(camera_shape, parent=True)[0]

            # Use short name
            name = cmds.ls(camera, long=False)[0].rsplit("_CAM", 1)[0]

            instance = context.create_instance(name=name, family="preview")
            instance.add(camera)
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

                instance.set_data(attr, value)

            # ftrack data
            components = {'preview': {'path': '',
                                      'reviewable': True,
                                      }}
            instance.set_data('ftrackComponents', value=components)
            self.log.info("Added: %s" % components)
