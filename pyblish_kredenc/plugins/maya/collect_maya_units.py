import pyblish.api

from maya import cmds
from maya import mel


@pyblish.api.log
class CollectMayaUnits(pyblish.api.Collector):
    """Collect Maya's scene units."""

    order = pyblish.api.Collector.order
    hosts = ["maya"]

    def process(self, context):

        # Get the current linear units
        units = cmds.currentUnit(q=1, linear=1)

        # Get the current angular units ('deg' or 'rad')
        units_angle = cmds.currentUnit(q=1, angle=1)

        # Get the current time units
        fps = mel.eval('currentTimeUnitToFPS()')

        context.set_data('linearUnits', units)
        context.set_data('angularUnits', units_angle)
        context.set_data('fps', fps)
