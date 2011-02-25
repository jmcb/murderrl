#!/usr/bin/env python
from library import coord
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
                  If none, identical to ``key``. *Default none*.
        :``key2``: An alternative activation key. *Default none*.
        """
        self.key    = key
        self.desc   = desc
        self.action = action
        self.key2   = key2

        if arg == None:
            self.arg = key
        else:
            self.arg = arg

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
