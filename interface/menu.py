#!/usr/bin/env python
import msvcrt

def getch ():
    """
    Windows specific method. Gets a key and returns it.
    """
    return msvcrt.getch()

def fill (num = 0):
    """
    Helper method printing clear lines to fill the screen.
    Will eventually be replaced by _clear() and _goto(x,y).

    :``num``: The number of lines already printed. *Default 0*.
    """
    if num > 24:
        return
    for i in range(num, 24):
        print ""

def clear ():
    """
    Helper method clearing the screen.
    Will eventually be replaced by _clear().
    """
    fill(0)

class Entry (object):
    """
    A representation of a menu entry.
    """
    def __init__ (self, key, desc, action, arg = None):
        """
        Initialize the entry.

        :``key``: The menu key for picking an entry. *Required*.
        :``desc``: The description of an entry. Together with the key, this forms
                   the string representation of an entry. *Required*.
        :``action``: What happens if the entry key is pressed. Points to a method
                     that takes a single argument, namely ``arg``. *Required*.
        :``arg``: The argument that is passed to action() when the entry is activated.
                  If none, identical to ``key``. *Default none*.
        """
        self.key    = key
        self.desc   = desc
        self.action = action
        if arg == None:
            self.arg = key
        else:
            self.arg = arg

    def __str__ (self):
        """
        Returns the entry in the form "key - desc".
        """
        return "%s - %s" % (self.key, self.desc)

    def activate (self):
        """
        Triggers the entry's action method, i.e. action(arg).
        """
        clear()
        self.action(self.arg)

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
        mlist = self.mlist
        lcount = 0
        if self.title:
            print self.title
            lcount += 1
        for i in xrange(len(mlist)):
            print mlist[i]
            lcount += 1
        fill(lcount)

    def process_key (self, key = None):
        """
        Compares the input with the entry keys and triggers the corresponding action.

        :``key``: The entered key. If none, call getch(). *Default none*.
        """
        if key == None:
            key = getch()

        mlist = self.mlist
        for i in xrange(len(mlist)):
            if mlist[i].key == key:
                mlist[i].activate()
                return True

        return False

    def do_menu (self):
        """
        Loop over drawing the menu and executing entry actions. Quits if the
        player presses a key that does not match any of the entries.
        """
        while True:
            clear()
            self.draw_menu()
            if not self.process_key():
                break
