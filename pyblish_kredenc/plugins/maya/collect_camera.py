import pyblish.api

import maya.cmds as cmds

@pyblish.api.log
class CollectCameras(pyblish.api.Collector):

    order = pyblish.api.Collector.order + 0.2
    hosts = ["maya"]
    label = "Collect Cameras"

    def process(self, context):

        if context.data['ftrackData']['Task']['type'] in ['Modelling']:
            return

        all_cameras = cmds.ls(objectsOnly=True,
                              type="camera",
                              long=True,
                              recursive=True)

        self.log.info(all_cameras)

        cameras = []
        for cam in all_cameras:
            if 'cam' in cam.lower():
                cameras.append(cam)

        for camera_shape in cameras:  # Include namespace

            camera = cmds.listRelatives(camera_shape, parent=True)[0]

            # Use short name
            name = cmds.ls(camera, long=False)[0].lower()

            instance = context.create_instance(name=name, family='camera')
            instance.add(camera)
            instance.data["publish"] = True

            item = name.split('_')[0]
            instance.data['item'] = item

            self.log.debug("item {}, name {}".format(item, name))

            if context.data['ftrackData']['Task']['type'] in ['Lighting']:
                instance.data['publish'] = True

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
