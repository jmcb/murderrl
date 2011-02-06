#!/usr/bin/env python
import msvcrt

def getch ():
    return msvcrt.getch()

def fill (num):
    if num > 24:
        return
    for i in range(num, 24):
        print ""

def clear ():
    fill(0)

class Entry (object):
    def __init__ (self, key, desc, action, val = None):
        self.key    = key
        self.desc   = desc
        self.action = action
        if val == None:
            self.val = key
        else:
            self.val = val

    def __str__ (self):
        return "%s - %s" % (self.key, self.desc)

    def activate (self):
        clear()
        self.action(self.val)
        if getch() == 0:
            getch()

class Menu (object):
    def __init__ (self, title = None):
        self.mlist = []
        self.title = title

    def add_entry (self, e):
        self.mlist.append(e)

    def draw_menu (self):
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
        if key == None:
            key = getch()

        mlist = self.mlist
        for i in xrange(len(mlist)):
            if mlist[i].key == key:
                mlist[i].activate()
                return True

        return False

    def do_menu (self):
        while True:
            clear()
            self.draw_menu()
            if not self.process_key():
                break
