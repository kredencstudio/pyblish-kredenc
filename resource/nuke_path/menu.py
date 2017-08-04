print 'executing pyblish-kredenc menu.py'

import nuke
import pyblish.api

nuke_menu = nuke.menu('Nuke')
file_menu = nuke_menu.findItem('File')
file_menu.addCommand("pyblish", 'pyblish_nuke.show()', "`")


pyblish.api.register_gui('pyblish_lite')
# pyblish.api.register_gui('pyblish_qml')
