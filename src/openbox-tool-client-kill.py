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
+ '<item label="Parar" icon="' + icondir +'/stop-b2a' + ext + '">'
+ '<action name="Execute">'
+ '<execute>kill -STOP ' + pid + '</execute></action></item>'
+ '<item label="Continuar" icon="' + icondir +'/spain_traffic_signal_r400c' + ext + '">'
+ '<action name="Execute">'
+ '<execute>kill -CONT ' + pid + '</execute></action></item>'
+ '<separator/>'
+ '<item label="Terminar" icon="' + icondir +'/exit' + ext + '">'
+ '<action name="Execute">'
+ '<execute>kill -TERM ' + pid + '</execute></action></item>'
+ '<item label="Matar" icon="' + icondir +'/bomba' + ext + '">'
+ '<action name="Execute">'
+ '<execute>kill -KILL ' + pid + '</execute></action></item>'

+ '</openbox_pipe_menu>'
)
