import os
import pyblish.api
import pyblish_kredenc.utils as pyblish_utils

class OpenOutputFolder(pyblish.api.Action):
    label = "Open folders"
    on = "processed"
    icon = "folder-open"

    def process(self, context, plugin):

        instances = pyblish_utils.filter_instances(context, plugin)

        for instance in instances:
            extractedPaths = [v for k,v in instance.data.items() if k.startswith('outputPath')]
            for path in extractedPaths:
                path = os.path.split(path)[0]
                self.log.info(path)
                pyblish_utils.open_folder(path)


class OpenOutputFile(pyblish.api.Action):
    label = "Open files"
    on = "processed"
    icon = "file"

    def process(self, context, plugin):

        instances = pyblish_utils.filter_instances(context, plugin)

        for instance in instances:
            extractedPaths = [v for k,v in instance.data.items() if k.startswith('outputPath')]
            for path in extractedPaths:
                self.log.info(path)
                pyblish_utils.open_folder(path)


class OpenPublishFolder(pyblish.api.Action):
    label = "Open Folder"
    on = "processed"
    icon = "folder-open"

    def process(self, context, plugin):

        instances = pyblish_utils.filter_instances(context, plugin)

        for instance in instances:
            extractedPaths = [v for k,v in instance.data.items() if k.startswith('publishFile')]
            for path in extractedPaths:
                path = os.path.split(path)[0]
                self.log.info(path)
                pyblish_utils.open_folder(path)
