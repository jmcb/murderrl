#!/usr/bin/env python
import sys, os

sys.path.append('../')

conf_file = open("doc.conf", "r")

toc = """
Table of Contents
=================
"""
contents = ""
cur_module = ""
cur_module_name = ""
cur_section = ""
cur_object = ""

num = 0
snum = 0
cnum = 0

class c(object): pass
def f (): pass

for line in conf_file:
    line = line.strip()
    if line.startswith("$module"):
        snum = 0
        num += 1
        cur_module = line.split()[1]
        cur_module_name = line.split(" ", 2)[2]
        if not globals().has_key(cur_module):
            globals()[cur_module] = __import__(cur_module)
        cur_module = globals()[cur_module]
        toc += "\n"
        toc += ("%s. `"+cur_module_name+"`_\n\n") % num
        contents += ".. _" +cur_module_name+":\n\n"
        contents += cur_module_name+"\n"
        contents += "=" * len(cur_module_name)+"\n\n"
        if cur_module.__doc__:
            for l in cur_module.__doc__.split("\n"):
                contents += l.lstrip() + "\n"
            contents += "\n\n"
    elif line.startswith("$section"):
        cnum = 0
        snum += 1
        cur_section = line.split()[1]
        toc += "\n"
        toc += (" %s. `"+cur_section+"`_\n") % chr(snum + 64)
        contents += ".. _"+cur_section+":\n\n"
        contents += cur_section+"\n"
        contents += "-" * len(cur_section)+"\n"
    else:
        cnum += 1
        cur_object = line
        obj = getattr(cur_module, cur_object)
        toc += "\n"
        toc += ("   %s. `"+cur_object+"`_\n") % chr(cnum + 96)
        contents += ".. _"+cur_object+":\n\n"
        if type(obj) == type(c):
            desc = "class *"
        elif type(obj) == type(f):
            desc = "function *"
        else:
            desc = "*"
        contents += desc + cur_object+"*\n"
        contents += "^" * (len(desc + cur_object)+1) +"\n"
        if obj.__doc__:
            for l in obj.__doc__.split("\n"):
                contents += l.lstrip() + "\n"
            contents += "\n\n"
        if type(obj) == type(c):
            contents += "Methods\n"
            contents += "#######\n\n"
            clnum = 0
            this_toc = ""
            this_contents = ""
            for method in dir(obj):
                method = getattr(obj, method)
                if hasattr(method, "im_class"):
                    clnum += 1
                    this_toc += "%s. `%s::%s`_.\n" % (clnum, obj.__name__, method.__name__)
                    this_contents += ".. _%s::%s:\n\n" % (obj.__name__, method.__name__)
                    this_contents += "**%s::%s**\n" % (obj.__name__, method.__name__)
                    if method.__doc__:
                        for l in method.__doc__.split("\n"):
                            this_contents += l.strip() + "\n\n"
                        this_contents += "\n"
                    else:
                        this_contents += "Method undocumented.\n\n"
            contents += this_toc + "\n\n"
            contents += this_contents

conf_file.close()

print toc, "\n", contents
