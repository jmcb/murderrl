#!/usr/bin/env python
"""
Each of the console libraries defines the following functions. The way these
functions are defined, access, etc, may differ across platforms and even through
implementations. For instance, pdcurses differs to curses which differs to
ncurses, all of which differ to the Windows API-based implementation.

put (char, c, colour=None)
==============================

Puts the contents of ``char`` on the screen at ``c.x/c.y``. It is assumed that
``c.x/c.y`` is within the bounds of the current screen. If ``colour`` is
provided, that value (an instance of Colour; see library.colour) will be used to
print the character.

:``char``: A single character, drawable to the screen. If ``None``, a space will
           be drawn instead.
:``c``: An instance of library.coord.Coord. Is presumed to be within the bounds
        of the current screen; indeed, attempting to put a character outside of
        the bounds of the screen will raise an exception.
:``colour``: An instance of library.colour.Colour. *Default None*.

get (err=False)
==================

Attempts to fetch a character from the standard input in a non-blocking manner.
If ``err`` is True, an exception will be raised if the function returns
before getting information from the standard input; otherwise, None will be
returned.

:``err``: If ``True``, the function will raise an InputError exception when
          achieving the end of the non-blocking read. If ``False``, ``None``
          will be returned instead.

clear (char=None, colour=None)
==============================

Wipes the contents of the screen, replacing all characters with ``char``, and,
if defined, using the colour ``colour``.

:``char``: This value will be bassed to ``put`` for every position on the
           screen. *Default None*.
:``colour``: This colour will be used as the colour for the text to be drawn.
             *Default None*.

size ()
=======

Returns an instance of library.coord.Size containing the dimensions of the
current screen size.

init ()
=======

Initialise the screen. For some interfaces, this may do nothing.

deinit ()
=========

De-initialise the screen. This function is always called before closing down the
current session. In some instances it may actually do nothing.
"""
import curse, win32

__provides__ = curse, win32

def select (priority="curse"):
    """
    Select a supported interface.
    """
    if not curse.UNAVAILABLE and (priority == "curse" or win32.UNAVAILABLE):
        return curse

    if not win32.UNAVAILABLE and (priority == "win32" or curse.UNAVAILABLE):
        return win32

    return None
