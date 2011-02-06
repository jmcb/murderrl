#!/usr/bin/env python
import library.coord as coord
import library.colour
import ctypes
from _subprocess import INFINITE, WAIT_OBJECT_0

OLD_SCREEN_SIZE = None

COMMON_LVB_UNDERSCORE = 32768
STD_INPUT_HANDLE = -10
STD_OUTPUT_HANDLE = -11
STD_ERROR_HANDLE = -12

WAIT_TIMEOUT = 0x102
WAIT_ABANDONED = 0x80

class _COORD(ctypes.Structure):
    _fields_ = [
        ("X", ctypes.c_short),
        ("Y", ctypes.c_short)]

class _SMALL_RECT(ctypes.Structure):
    _fields_ = [
        ("Left", ctypes.c_short),
        ("Top", ctypes.c_short),
        ("Right", ctypes.c_short),
        ("Bottom", ctypes.c_short)]

class _CONSOLE_SCREEN_BUFFER_INFO(ctypes.Structure):
    _fields_ = [
        ("dwSize", _COORD),
        ("dwCursorPosition", _COORD),
        ("wAttributes", ctypes.c_ushort),
        ("srWindow", _SMALL_RECT),
        ("dwMaximumWindowSize", _COORD)]

class _CONSOLE_CURSOR_INFO (ctypes.Structure):
    _fields_ = [
        ("dwSize", ctypes.c_ushort),
        ("bVisible", ctypes.c_bool)]

class _FOCUS_EVENT_RECORD (ctypes.Structure):
    _fields_ = [
        ("bSetFocus", ctypes.c_bool)]

class _UCHAR (ctypes.Union):
    _fields_ = [
        ("UnicodeChar", ctypes.c_char),
        ("AsciiChar", ctypes.c_wchar)]

class _KEY_EVENT_RECORD (ctypes.Structure):
    _fields_ = [
        ("bKeyDown", ctypes.c_bool),
        ("wRepeatCount", ctypes.c_ushort),
        ("wVirtualKeyCode", ctypes.c_ushort),
        ("wVirtualScanCode", ctypes.c_ushort),
        ("uChar", _UCHAR),
        ("dwControlKeyState", ctypes.c_uint)]

class _MENU_EVENT_RECORD (ctypes.Structure):
    _fields_ = [
        ("dwCommandId", ctypes.c_uint)]

class _MOUSE_EVENT_RECORD (ctypes.Structure):
    _fields_ = [
        ("dwMousePosition", _COORD),
        ("dwButtonState", ctypes.c_uint),
        ("dwControlKeyState", ctypes.c_uint),
        ("dwEventFlags", ctypes.c_uint)]

class _WINDOW_BUFFER_SIZE_RECORD (ctypes.Structure):
    _fields_ = [
        ("dwSize", _COORD)]

class _EVENT (ctypes.Union):
    _fields_ = [
        ("KeyEvent", _KEY_EVENT_RECORD),
        ("MouseEvent", _MOUSE_EVENT_RECORD),
        ("WindowBufferSizeEvent", _WINDOW_BUFFER_SIZE_RECORD),
        ("MenuEvent", _MENU_EVENT_RECORD),
        ("FocusEvent", _FOCUS_EVENT_RECORD)]

class _INPUT_RECORD (ctypes.Structure):
    _fields_ = [
        ("EventType", ctypes.c_ushort),
        ("Event", _EVENT)]

class DOSBaseColour (library.colour.BaseColour):
    def __init__ (self, colour):
        super(DOSBaseColour, self).__init__(colour._colour, colour._colour_id)

    def is_background ():
        if self._colour_id == 0x0000:
            return True

        return self._colour_id & 0x0070

    def is_foreground ():
        if self._colour_id == 0x0000:
            return True

        return self._colour_id & 0x0007

    def as_background ():
        if self.is_background():
            return self._colour_id & 0x0070

        return self._colour_id & 0x0007 << 4

    def as_foreground ():
        if self.is_foreground():
            return self._colour_id & 0x0007

        return self._colour_id & 0x0070 >> 4

class DOSColour (library.colour.Colour):
    def __init__ (self, colour):
        super(DOSColour, self).__init__(colour._foreground, colour._background, colour._style)

    def as_dos ():
        fg = DOSBaseColour(self._foreground).as_foreground()
        bg = DOSBaseColour(self._background).as_background()

        new_col = fg | bg

        if self._style == "underline":
            new_col |= COMMON_LVB_UNDERSCORE

        return new_col

def _STDOUT ():
    return _GetStdHandle(STD_OUTPUT_HANDLE)

def _STDIN ():
    return _GetStdHandle(STD_INPUT_HANDLE)

def _STDERR ():
    return _GetStdHandle(STD_ERROR_HANDLE)

def _GetStdHandle (handle):
    return ctypes.windll.kernel32.GetStdHandle(handle)

def _GetColour ():
    return _GetConsoleScreenBufferInfo().wAttributes

def _GetBG ():
    return _GetConsoleScreenBufferInfo().wAttributes & 0x0070

def _GetFG ():
    return _GetConsoleScreenBufferInfo().wAttributes & 0x0007

def _WaitForMultipleObjects (handles, wait_all=False, wtime=INFINITE):
    return ctypes.windll.kernel32.WaitForMultipleObjects(len(handles), (ctypes.c_int*len(handles))(*handles), ctypes.c_bool(wait_all), wtime)

def _GetConsoleScreenBufferInfo ():
    buffer_info = _CONSOLE_SCREEN_BUFFER_INFO()
    ctypes.windll.kernel32.GetConsoleScreenBufferInfo(_STDOUT(), ctypes.byref(buffer_info))
    return buffer_info

def _GetConsoleCursorInfo ():
    cursor_info = _CONSOLE_CURSOR_INFO()
    ctypes.windll.kernel32.GetConsoleCursorInfo(_STDOUT(), ctypes.byref(cursor_info))
    return cursor_info

def _SetColour (colour, dos=False):
    if not dos:
        colour = DOSColour(colour).as_dos()
    return ctypes.windll.kernel32.SetConsoleTextAttribute(_STDOUT(), colour)

def _SetConsoleCursorInfo (size=1, visible=True):
    cursor_info = _CONSOLE_CURSOR_INFO()
    cursor_info.dwSize = size
    cursor_info.bVisible = ctypes.c_bool(visible)
    return ctypes.windll.kernel32.SetConsoleCursorInfo(_STDOUT(), cursor_info)

def _SetConsoleSize (c=None):
    if c is None:
        c = _GetConsoleScreenBufferInfo().dwSize
        c.Y = 25

    if not isinstance(c, _COORD):
        c = _COORD(c.x, c.y)

    return ctypes.windll.kernel32.SetConsoleScreenBufferSize(_STDOUT(), c)

def _goto (c):
    if not isinstance(c, _COORD):
        c = _COORD(c.x, c.y)
    return ctypes.windll.kernel32.SetConsoleCursorPosition(_STDOUT(), c)

def _getxy ():
    return _GetConsoleScreenBufferInfo().dwCursorPosition

def put (char, c, colour=None):
    _goto(c)
    old_c = _getxy()
    old_colour = _GetColour()
    if colour is not None:
        _SetColour(colour)

    print char

    _goto(old_c)
    _SetColour(old_colour, True)

def get (err=False, block=False):
    pass

def clear (char=None, colour=None):
    termsize = size()

    if char is None:
        char = " "

    for x in xrange(termsize.width):
        for y in xrange(termsize.height):
            put (char, coord.Coord(x, y), colour)

def init ():
    global OLD_SCREEN_SIZE
    OLD_SCREEN_SIZE = _GetConsoleScreenBufferInfo().dwSize
    OLD_SCREEN_SIZE = coord.Coord(OLD_SCREEN_SIZE.X, OLD_SCREEN_SIZE.Y)
    _SetConsoleSize()

def deinit ():
    _SetConsoleSize(OLD_SCREEN_SIZE)

def size ():
    info = _GetConsoleScreenBufferInfo().dwSize
    size = coord.Size()
    size.width = info.X
    size.height = info.Y
    return size

def wrapper (fn):
    try:
        fn()
    except:
        deinit()
        raise

    deinit()
