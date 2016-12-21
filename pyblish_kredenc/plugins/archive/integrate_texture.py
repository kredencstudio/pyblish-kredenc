import os

import pyblish.api
import pymel


class IntegrateTexture(pyblish.api.Integrator):
    """
    """

    families = ['texture']

    def process(self, instance):

        currentFolder = instance.context.data['currentFile']




        self.log.info(currentFolder)
