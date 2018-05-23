import os
import json
import re

import pyblish.api
from Deadline.Scripting import *


class CollectMovieDraft(pyblish.api.InstancePlugin):
    """ Generate movie job """

    order = pyblish.api.CollectorOrder + 0.1
    families = ["render"]

    def process(self, instance):

        # prevent render files to generate movies
        if os.path.splitext(instance.data["family"])[1] in [".ifd"]:
            return

        job = instance.context.data("deadlineJob")
        data = job.GetJobExtraInfoKeyValueWithDefault("PyblishInstanceData",
                                                      "")
        if not data:
            return

        data = json.loads(data)

        for path in instance.data["files"]:

            if '_mask' in path:
                return

            new_instance = instance.context.create_instance(name=str(instance))

            for key in data:
                instance.data[key] = data[key]
                if 'ftrack' in key:
                    new_instance.data[key] = data[key]
                    if 'ftrackComponents' in key:
                        for component in data[key]:
                            if component in ['main', 'beauty']:
                                new_instance.data['ftrackComponents'] = {
                                    "review": {"reviewable": True}}
                            else:
                                new_instance.data['ftrackComponents'] = {
                                    component + '_movie': {}}

            # prevent resubmitting same job
            del instance.data["deadlineData"]
            instance.data["families"].remove("deadline")

            new_instance.data["family"] = "mov.farm.mov"
            new_instance.data["families"] = ["mov.*", "mov.farm.*", "deadline"]
            new_instance.data["files"] = {}


            #regex .%..d + (_|).#{2,20}

            output_path = re.sub(r'.%..d', '', path)
            output_path = re.sub(r"(_|).#{2,20}", '', output_path)
            output_path = os.path.splitext(output_path)[0] + ".mov"
            output_folder = os.path.split(output_path)[0]
            start_frame = str(job.JobFramesList[0])
            end_frame = str(job.JobFramesList[-1])
            frame_list = '{}-{}'.format(start_frame, end_frame)

            # ensure hashes in filename
            path = FrameUtils.ReplacePaddingWithFrameNumber(path, 1)
            path = FrameUtils.ReplaceFrameNumberWithPadding(path, '#')

            # setting job data
            job_data = {}
            job_data["Plugin"] = "DraftPlugin"
            job_data["Frames"] = frame_list
            job_data["Name"] = job.Name
            job_data['Pool'] = 'comp'
            job_data['Group'] = 'draft'
            job_data['Priority'] = job.Priority + 1
            job_data["UserName"] = job.UserName
            job_data["OutputFilename0"] = output_path
            job_data["ChunkSize"] = job.JobFramesList[-1]

            # setting plugin data
            plugin_data = {}
            plugin_data["scriptFile"] = r'\\kre-c01\share\core\dev\deadline-custom\draft\encode_to_MOV_H264_1080p_with_audio.py'
            plugin_data["ScriptArg0"] = "username=\"\""
            plugin_data["ScriptArg1"] = "entity=\"\""
            plugin_data["ScriptArg2"] = "version=\"\""
            plugin_data["ScriptArg3"] = "isDistributed=\"False\""
            plugin_data["ScriptArg4"] = "frameList={}".format(frame_list)
            plugin_data["ScriptArg5"] = "startFrame={}".format(start_frame)
            plugin_data["ScriptArg6"] = "endFrame={}".format(end_frame)
            plugin_data["ScriptArg7"] = "outFolder=\"{}\"".format(output_folder)
            plugin_data["ScriptArg8"] = "outFile=\"{}\"".format(output_path)
            plugin_data["ScriptArg9"] = "inFile=\"{}\"".format(path)


            # setting data
            data = {"job": job_data, "plugin": plugin_data}
            new_instance.data["deadlineData"] = data

            self.log.info("Instance name: " + new_instance.name)
            self.log.info("Families: " + str(new_instance.data["families"]))
            self.log.info("data: " + str(new_instance.data))
