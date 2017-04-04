#!/usr/bin/env python
# 20170228. Port to python3
#20152601
# If probrems try to delete ~/.Xauthority and restart xsession

from Xlib import display, X, protocol

display = display.Display()
root = display.screen().root


def getprop(prop, win=None):
    if not win: win = root
    atom = win.get_full_property(display.get_atom(prop), X.AnyPropertyType)
    if atom: return atom.value


def setprop(prop, data, win=None, mask=None):
    """ Send a ClientMessage event to the root """
    if not win: win = root
    if type(data) is str:
        dataSize = 8
    else:
        data = (data+[0]*(5-len(data)))[:5]
        dataSize = 32

    ev = protocol.event.ClientMessage(window=win, client_type=display.get_atom(prop), data=(dataSize, data))

    if not mask:
        mask = (X.SubstructureRedirectMask|X.SubstructureNotifyMask)
    root.send_event(ev, event_mask=mask)


def setMoveResizeWindow(win, gravity=0, x=None, y=None, w=None, h=None):
    """Set the property _NET_MOVERESIZE_WINDOW to move / resize the given window.
    Flags are automatically calculated if x, y, w or h are defined.

    :param win: the window object
    :param gravity: gravity (one of the Xlib.X.*Gravity constant or 0)
    :param x: int or None
    :param y: int or None
    :param w: int or None
    :param h: int or None"""
    gravity_flags = gravity | 0b0000100000000000 # indicate source (application)
    if x is None: x = 0
    else: gravity_flags = gravity_flags | 0b0000010000000000 # indicate presence of x
    if y is None: y = 0
    else: gravity_flags = gravity_flags | 0b0000001000000000 # indicate presence of y
    if w is None: w = 0
    else: gravity_flags = gravity_flags | 0b0000000100000000 # indicate presence of w
    if h is None: h = 0
    else: gravity_flags = gravity_flags | 0b0000000010000000 # indicate presence of h
    setprop('_NET_MOVERESIZE_WINDOW', [gravity_flags, x, y, w, h], win)


def setWmState(win, action, state, state2=0):
    """Set / unset one or two state(s) for the given window (property _NET_WM_STATE).

    :param win: the window object
    :param action: 0 to remove, 1 to add or 2 to toggle state(s)
    :param state: a state
    :type state: int or str (see :attr:`NET_WM_STATES`)
    :param state2: a state or 0
    :type state2: int or str (see :attr:`NET_WM_STATES`)"""
    if type(state) != int: state = display.get_atom(state, 1)
    if type(state2) != int: state = display.get_atom(state2, 1)
    setprop('_NET_WM_STATE', [action, state, state2, 1], win)

awin = getprop('_NET_ACTIVE_WINDOW')[0]
cdesk = getprop('_NET_CURRENT_DESKTOP')[0]

worka = getprop('_NET_WORKAREA')
wax = worka[0 + 4 * cdesk]
way = worka[1 + 4 * cdesk]
waw = worka[2 + 4 * cdesk]
wah = worka[3 + 4 * cdesk]

gravity = 0
w = waw * 80 / 100
h = wah * 80 / 100
x = waw / 2 - w / 2
y = wah / 2 - h / 2

setWmState(awin, 0, '_NET_WM_STATE_MAXIMIZED_VERT')
setWmState(awin, 0, '_NET_WM_STATE_MAXIMIZED_HORZ')
setWmState(awin, 0, '_NET_WM_STATE_SHADED')
setMoveResizeWindow(awin, gravity, x, y, w, h)

display.flush()
