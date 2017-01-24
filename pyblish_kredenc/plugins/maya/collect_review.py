import pyblish.api

import maya.cmds as cmds

@pyblish.api.log
class CollectPreview(pyblish.api.ContextPlugin):

    order = pyblish.api.CollectorOrder + 0.2
    hosts = ["maya"]
    label = "Collect Review"

    def process(self, context):

        all_cameras = cmds.ls(objectsOnly=True,
                              type="camera",
                              long=True,
                              recursive=True)

        self.log.info(all_cameras)

        cameras = []
        for cam in all_cameras:
            if 'cam' in cam.lower():
                cameras.append(cam)

        cameras.append('perspShape')

        for camera_shape in cameras:  # Include namespace

            camera = cmds.listRelatives(camera_shape, parent=True)[0]

            # Use short name
            name = cmds.ls(camera, long=False)[0].lower().rsplit("_cam", 1)[0]

            instance = context.create_instance(name=name, family='review')
            instance.add(camera)
            instance.data["families"] = ['review']
            instance.data["label"] = name + ' camera'

            if camera == 'persp':
                instance.data['publish'] = False

            if context.data['ftrackData']['Task']['type'] in ['Lighting']:
                instance.data['publish'] = False

            attrs = cmds.listAttr(camera, userDefined=True) or list()

            self.log.info("Found: %s" % camera)
            self.log.info("Overrides: %s" % attrs)

            # task specific overrides
            if context.data['ftrackData']['Task']['type'] == 'Rigging':
                instance.data['show'] = ['polymeshes', 'nurbsCurves', 'joints']


            # ftrack data
            components = {'review': {'path': '',
                                     'reviewable': True,
                                     }}
            instance.data['ftrackComponents'] = components

            self.log.info("Added: %s" % components)
            self.log.info("components: %s" % instance.data['ftrackComponents'])
