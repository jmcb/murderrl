#!/usr/bin/env python
import curses
from library import coord, shape, collection, viewport
from interface import console
from output import *

screen = console.select()

class Entry (object):
    """
    A representation of a menu entry.
    """
    def __init__ (self, key, desc, action, arg = None, key2 = None):
        """
        Initialize the entry.

        :``key``: The menu key for picking an entry. *Required*.
        :``desc``: The description of an entry. Together with the key, this forms
                   the string representation of an entry. *Required*.
        :``action``: What happens if the entry key is pressed. Points to a method
                     that takes a single argument, namely ``arg``. *Required*.
        :``arg``: The argument that is passed to action() when the entry is activated.
                  *Default none*.
        :``key2``: An alternative activation key. *Default none*.
        """
        self.key    = key
        self.desc   = desc
        self.action = action
        self.arg    = arg
        self.key2   = key2

    def __str__ (self):
        """
        Returns the entry in the form "key - desc".
        """
        return "%s - %s" % (self.key, self.desc)

    def key_matches (self, key):
        """
        Returns true if a given character matches the entry key.

        :``key``: The character to compare against the entry key. *Required*.
        """
        return (self.key == key or self.key2 == key)

    def activate (self):
        """
        Triggers and returns the entry's action method, i.e. action(arg).
        """
        if self.arg == None:
            return self.action()
        else:
            return self.action(self.arg)

class Menu (object):
    """
    A representation of a menu entry, built up of a list of type Entry[].
    """
    def __init__ (self, title = None):
        """
        Initialize the menu.
        The menu itself, represented by ``mlist``, is initially empty.

        :``title``: A header for the menu display. *Default none*.
        """
        self.mlist = []
        self.title = title

    def add_entry (self, entry):
        """
        Adds a menu entry.

        :``entry``: A menu entry of type ``Entry``. *Required*.
        """
        self.mlist.append(entry)

    def draw_menu (self):
        """
        Prints the entire menu on an otherwise empty screen.
        """
        screen.clear(" ")
        line = 0
        if self.title:
            print_line(self.title)
            line = 1

        mlist = self.mlist
        for i in xrange(len(mlist)):
            print_line(mlist[i].__str__(), coord.Coord(0, line + i))

    def process_key (self, key = None):
        """
        Compares the input with the entry keys and triggers the corresponding action.
        This action is currently assumed to return a string that is subsequently
        printed to the screen.

        :``key``: The entered key. If none, call get(). *Default none*.
        """
        if key == None:
            key = screen.get(block=True)

        mlist = self.mlist
        for i in xrange(len(mlist)):
            if mlist[i].key_matches(chr(key)):
                fulldesc = mlist[i].activate()
                if fulldesc:
                    print_screen(fulldesc)
                return True

        return False

    def do_menu (self):
        """
        Loop over drawing the menu and executing entry actions. Quits if the
        player presses a key that does not match any of the entries.
        """
        while True:
            self.draw_menu()
            if not self.process_key():
                break

class ScrollMenu (Menu):
    # def __init__ (self, title = None):
        # Menu.__init__(self, title)

    def write_on_canvas (self, text, line = 0):
        for ind, char in enumerate(text):
            if ind >= self.canvas.size().x:
                return
            self.canvas.__setitem__(coord.Coord(ind, line), char)

    def paint_canvas (self):
        rows = len(self.mlist)
        if self.title:
            rows += 1
        self.canvas = shape.Shape(width=60, height=rows, fill=" ")
        line = 0
        if self.title:
            self.write_on_canvas(self.title)
            line = 1

        mlist = self.mlist
        for i in xrange(len(mlist)):
            self.write_on_canvas(mlist[i].__str__(), line + i)

    def draw_menu (self):
        screen.clear(" ")
        sect = self.vp.sect()
        for pos, char in sect:
            if char == None:
                char = " "
            screen.put(char, pos+1)
        self.write_scrolling_help()

    def write_scrolling_help (self):
        scrollkeys = []
        if self.vp._top > 0:
            scrollkeys.append("up")
        if self.vp._top + self.vp._height < self.canvas.size().y:
            scrollkeys.append("down")
        if len(scrollkeys) > 0:
            keys = '/'.join(scrollkeys)
            plural_s = "s"
            if len(scrollkeys) == 1:
                plural_s = ""
            print_line("[scroll with %s key%s]" % (keys, plural_s), coord.Coord(0, self.rows+1))

    def process_key (self, key = None):
        """
        Compares the input with the entry keys and triggers the corresponding action.
        This action is currently assumed to return a string that is subsequently
        printed to the screen.

        :``key``: The entered key. If none, call get(). *Default none*.
        """
        if key == None:
            key = screen.get(block=True)

        if key == curses.KEY_UP:
            if self.vp._top > 0:
                self.vp.up(1)
        elif key == curses.KEY_DOWN:
            if self.vp._top + self.vp._height < self.canvas.size().y:
                self.vp.down(1)
        else:
            mlist = self.mlist
            for i in xrange(len(mlist)):
                if mlist[i].key_matches(chr(key)):
                    fulldesc = mlist[i].activate()
                    if fulldesc:
                        print_screen(fulldesc)
                    return True
            return False

        return True

    def do_menu (self):
        self.paint_canvas()
        self.rows = min(15, self.canvas.size().y)
        self.vp = viewport.ViewPort(buffer=self.canvas, width=70, height=self.rows)

        while True:
            self.draw_menu()
            if not self.process_key():
                break
