import os
import sys
import pyblish.api


def open_folder(path):
    import subprocess
    path = os.path.abspath(path)
    if sys.platform == 'win32':
        subprocess.Popen('explorer "%s"' % path)
    elif sys.platform == 'darwin':  # macOS
        subprocess.Popen(['open', path])
    else:  # linux
        try:
            subprocess.Popen(['xdg-open', path])
        except OSError:
            raise OSError('unsupported xdg-open call??')


def filter_instances(context, plugin):
    # Get the errored instances
    allInstances = []
    for result in context.data["results"]:
        if (result["instance"] is not None and
           result["instance"] not in allInstances):
            allInstances.append(result["instance"])

    # Apply pyblish.logic to get the instances for the plug-in
    instances = pyblish.api.instances_by_plugin(allInstances, plugin)

    return instances


class OpenOutputFolder(pyblish.api.Action):
    label = "Open folders"
    on = "processed"
    icon = "folder-open"

    def process(self, context, plugin):

        instances = filter_instances(context, plugin)

        for instance in instances:
            extractedPaths = [v for k,v in instance.data.items() if k.startswith('outputPath')]
            for path in extractedPaths:
                path = os.path.split(path)[0]
                self.log.info(path)
                open_folder(path)


class OpenOutputFile(pyblish.api.Action):
    label = "Open files"
    on = "processed"
    icon = "file"

    def process(self, context, plugin):

        instances = filter_instances(context, plugin)

        for instance in instances:
            extractedPaths = [v for k,v in instance.data.items() if k.startswith('outputPath')]
            for path in extractedPaths:
                self.log.info(path)
                open_folder(path)

class OpenPublishFolder(pyblish.api.Action):
    label = "Open Folder"
    on = "processed"
    icon = "folder-open"

    def process(self, context, plugin):

        instances = filter_instances(context, plugin)

        for instance in instances:
            extractedPaths = [v for k,v in instance.data.items() if k.startswith('publishFile')]
            for path in extractedPaths:
                path = os.path.split(path)[0]
                self.log.info(path)
                open_folder(path)
