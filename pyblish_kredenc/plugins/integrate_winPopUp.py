import pyblish.api
import ftrack
from win10toast import ToastNotifier




import os

import ftrack_api
reload(ftrack_api)


def giveMeInfo():
    shotId = os.getenv('FTRACK_SHOTID')
    taskId = os.getenv('FTRACK_TASKID')

    session = ftrack_api.Session()
    shot = session.query('Shot where id is {}'.format(shotId)).one()
    shotName = shot['name']
    handles = int(shot['custom_attributes']['handles'])
    sf = int(shot['custom_attributes']['fstart'])
    ef = int(shot['custom_attributes']['fend'])

    task = session.query('Task where id is {}'.format(taskId)).one()
    taskName = task['name']

    return[shotName,taskName]



class WinPopUp(pyblish.api.InstancePlugin):
    """ Show windows 10 notify balloon. """

    order = pyblish.api.IntegratorOrder + 0.45
    label = "winPopUp"
    optional = True

    def process(self, instance):

        # Skipping instance if ftrackData isn"t present.
        if not instance.context.has_data("ftrackData"):
            msg = "No ftrackData present. "
            msg += "Skipping this instance: \"%s\"" % instance
            self.log.info(msg)
            return

        infoStr = giveMeInfo()

        toaster = ToastNotifier()
        toaster.show_toast("Task {0} from shot {1}".format(infoStr[1], infoStr[0]),
                           "Pyblished Completed",
                           #icon_path= iconPath,
                           duration = 10,
                           threaded=True)
