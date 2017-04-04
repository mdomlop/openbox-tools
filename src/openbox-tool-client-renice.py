#!/usr/bin/env python
# 20170228. Port to python3
#20150126

from Xlib import display, X, protocol, Xatom
import time
from os import environ

icondir = environ['OPENBOX_ICONDIR']
ext = '.svg'

class EWMH:
    def __init__(self, _display=None, root = None):
        self.display = _display or display.Display()
        self.root = root or self.display.screen().root

    def getActiveWindow(self):
        """Get the current active (toplevel) window or None (property _NET_ACTIVE_WINDOW)

        :return: Window object or None"""
        return self._createWindow(self._getProperty('_NET_ACTIVE_WINDOW')[0])

    def getWmPid(self, win):
        """Get the pid of the application associated to the given window (property _NET_WM_PID)

        :param win: the window objet"""
        return self._getProperty('_NET_WM_PID', win)[0]

    def _getProperty(self, _type, win=None):
        if not win: win = self.root
        atom = win.get_full_property(self.display.get_atom(_type), X.AnyPropertyType)
        if atom: return atom.value

    def _createWindow(self, wId):
        if not wId: return None
        return self.display.create_resource_object('window', wId)


wm = EWMH()
awin = wm.getActiveWindow()
pid = str(wm.getWmPid(awin))

print(
'<openbox_pipe_menu>'
+ '<separator label="Proceso: ' + pid + '"/>'
+ '<item label="Incrementar en 5" icon="' + icondir +'/sumar' + ext + '">'
+ '<action name="Execute">'
+ '<execute>renice +5 ' + pid + '</execute></action></item>'
+ '<item label="Decrementar en 5" icon="' + icondir +'/restar' + ext + '">'
+ '<action name="Execute">'
+ '<execute>renice -5 ' + pid + '</execute></action></item>'
+ '<separator/>'
+ '<item label="Normal" icon="' + icondir +'/face-plain' + ext + '">'
+ '<action name="Execute">'
+ '<execute>renice 0 ' + pid + '</execute></action></item>'
+ '<separator/>'
+ '<item label="Mínima actividad" icon="' + icondir +'/face-grin' + ext + '">'
+ '<action name="Execute">'
+ '<execute>renice 20 ' + pid + '</execute></action></item>'
+ '<item label="Máxima actividad" icon="' + icondir +'/face-angry' + ext + '">'
+ '<action name="Execute">'
+ '<execute>renice -20 ' + pid + '</execute></action></item>'
+ '</openbox_pipe_menu>'
)
