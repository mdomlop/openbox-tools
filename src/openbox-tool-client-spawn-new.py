#!/usr/bin/env python

# Spawn a new client.

# 20170228

from Xlib import display, X, protocol, Xatom
import time
import os

icondir = os.environ['OPENBOX_ICONDIR']
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

cmdline_file = open(os.path.join('/proc', str(pid), 'cmdline'), 'r')
cmdline_file_content=cmdline_file.read()
cmdline_file.close()
cmdline=cmdline_file_content.split("\x00")[0]

os.system(cmdline)

