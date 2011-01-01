#!/usr/bin/env python
import sys, os
import inspect

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

class c(object): pass
def f (): pass

class Document:
    modules = []
    ignore = []
    def __iter__ (self):
        for module in self.modules:
            yield module, None, None
            for section in module.sections:
                yield module, section, None
                for classes in section.classes:
                    yield module, section, classes
                for method in section.methods:
                    yield module, section, method

    def __str__ (self):
        result = "Document:\n"
        for module, section, obj in self:
            if section is None and obj is None:
                result += " -%s\n" % module.name
            elif section is not None and obj is None:
                result += "  -%s (classes)\n" % section.name
                x = True
            else:
                if inspect.isfunction(obj) and x == True:
                    result += "  -%s (methods)\n" % section.name
                    x = False
                result += "   -%s\n" % obj.__name__
        return result

class Module:
    module = None
    name = None
    sections = None
    def __init__ (self, name=None):
        self.name = name
        self.module = None
        self.sections = []
    def __repr__ (self):
        return "<Module name=%s>" % self.name

class Section:
    name = None
    classes = None
    methods = None
    def __init__ (self, name=None):
        self.name = name
        self.classes = []
        self.methods = []
    def __repr__ (self):
        return "<Section name=%s, classes=%s, methods=%s>" % (self.name, self.classes, self.methods)

def docparser (filename, verbose=False):
    if isinstance(filename, file):
        x = [x.strip() for x in filename.readlines()]
        filename.close()
        filename = x
    elif isinstance(filename, str):
        if "\n" in filename:
            filename = filename.split("\n")
        else:
            x = open(filename, 'r')
            filename = x.readlines()
            x.close()
    else:
        raise Exception, "Unexpected type for docparser: %s." % type(filename)
    doc = Document()
    cur_module = None
    cur_section = None
    for line in filename:
        line = line.strip()
        if line.startswith("$module"):
            if cur_module is not None:
                doc.modules.append(cur_module)
            cur_module = Module()
            cur_module.module = __import__(line.split(" ", 2)[1])
            cur_module.name = line.split(" ", 2)[2]
            if verbose:
                print cur_module
        elif line.startswith("$section"):
            if cur_section is not None:
                cur_module.sections.append(cur_section)
            cur_section = Section()
            cur_section.name = line.split()[1]
            if verbose:
                print cur_section
        elif line.startswith("$classes"):
            class_list = line.split(" ", 1)[1].split(", ")
            for c in class_list:
                if verbose:
                    print "<Class %s>" % c
                if c == "None":
                    cur_section.classes.append(None)
                    break
                else:
                    cur_section.classes.append(getattr(cur_module.module, c))
        elif line.startswith("$methods"):
            method_list = line.split(" ", 1)[1].split(", ")
            for m in method_list:
                print "Methods: " + m
                if m == "None":
                    cur_section.methods.append(None)
                    break
                else:
                    cur_section.methods.append(getattr(cur_module.module, m))
        elif line.startswith("$ignore"):
            if verbose:
                print "<Ignore %s>" % line.split()[1]
            doc.ignore.append(line.split()[1])
        else:
            if verbose:
                print "Unknown symbol: " + line
    return doc

def main ():
    snum = 0
    num = 0
    cnum = 0

    parsed = docparser("doc.conf")
    toc = ""
    contents = ""

    for module, section, obj in parsed:
        if section is None and obj is None:
            snum = 0
            num += 1
            toc += "\n"
            toc += ("%s. `"+module.name+"`_\n\n") % num
            contents += ".. _" +module.name+":\n\n"
            contents += module.name+"\n"
            contents += "=" * len(module.name)+"\n\n"
            if module.module.__doc__:
                for l in module.module.__doc__.split("\n"):
                    contents += l.lstrip() + "\n"
                contents += "\n\n"
        elif section is not None and obj is None:
            cnum = 0
            snum += 1
            toc += "\n"
            toc += (" %s. `"+section.name+"`_\n") % chr(snum + 64)
            contents += ".. _"+section.name+":\n\n"
            contents += section.name+"\n"
            contents += "-" * len(section.name)+"\n"
        elif obj is not None:
            cur_object = obj.__name__
            toc += "\n"
            toc += ("   %s. `"+cur_object+"`_\n") % chr(cnum + 96)
            contents += ".. _"+cur_object+":\n\n"
            if inspect.isclass(obj):
                desc = "class *"
            elif inspect.isfunction(obj):
                desc = "function *"
            else:
                desc = "*"
            contents += desc + cur_object+"*\n"
            contents += "^" * (len(desc + cur_object)+1) +"\n"
            if obj.__doc__:
                for l in obj.__doc__.split("\n"):
                    contents += l.lstrip() + "\n"
                contents += "\n\n"
            if inspect.isclass(obj):
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
                                this_contents += l.strip() + "\n"
                            this_contents += "\n"
                        else:
                            this_contents += "Method undocumented.\n\n"
                contents += this_toc + "\n\n"
                contents += this_contents

    print toc, "\n", contents

if __name__=="__main__":
    main()
