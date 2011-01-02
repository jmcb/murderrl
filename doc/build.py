#!/usr/bin/env python
import sys, os
import inspect

sys.path.append('../')

conf_file = open("doc.conf", "r")

divider = "\n" + "~" * 80 + "\n"

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
                if len(section.classes) != 0:
                    for classes in section.classes:
                        yield module, section, classes
                if len(section.methods) != 0:
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
            if cur_section is not None and cur_section not in cur_module.sections:
                cur_module.sections.append(cur_section)
                cur_section = None
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
                    break
                else:
                    cur_section.classes.append(getattr(cur_module.module, c))
        elif line.startswith("$methods"):
            method_list = line.split(" ", 1)[1].split(", ")
            for m in method_list:
                if verbose:
                    print "Methods: " + m
                if m == "None":
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
    if cur_section is not None and cur_section not in cur_module.sections:
        cur_module.sections.append(cur_section)
    doc.modules.append(cur_module)
    return doc

#####################################################################
#####################################################################
# Actual doc generation goes from here down.

def main ():
    snum = 0
    num = 0
    cnum = 0

    toc = """\nTable of Contents\n=================\n"""
    contents = ""

    parsed = docparser("doc.conf")

    for module, section, obj in parsed:
        if section is None and obj is None:
            snum = 0
            num += 1
            toc += "\n"
            toc += ("%s. `"+module.name+"`_\n") % num
            contents += "\n.. _" +module.name+":\n\n"
            contents += module.name+"\n"
            contents += "=" * len(module.name)+"\n"
            if module.module.__doc__:
                contents += "\n" + inspect.getdoc(module.module) + "\n"
            contents += divider
        elif section is not None and obj is None:
            cnum = 0
            snum += 1
            toc += "\n"
            toc += ("  %s. `"+section.name+"`_\n\n") % chr(snum + 64)
            contents += "\n.. _"+section.name+":\n\n"
            contents += section.name+"\n"
            contents += "-" * len(section.name)+"\n"
        elif obj is not None:
            cnum += 1
            cur_object = obj.__name__
            toc += ("    %s. `"+cur_object+"`_\n") % chr(cnum + 96)
            contents += "\n.. _"+cur_object+":\n\n"
            if inspect.isclass(obj):
                desc = "class *%s*" % cur_object
            elif inspect.isfunction(obj):
                desc = "function *%s* %s" % (cur_object, inspect.formatargspec(*inspect.getargspec(obj)))
            else:
                desc = "*%s*" % cur_object
            contents += desc + "\n"
            contents += ("^" * len(desc)) +"\n"
            if obj.__doc__:
                contents += "\n" + inspect.getdoc(obj) + "\n"
            if inspect.isclass(obj):
                clnum = 0
                this_toc = ""
                this_contents = ""
                attrs = inspect.classify_class_attrs(obj)
                attrs = [x for x in attrs if x.kind == "method" and inspect.ismethod(getattr(obj, x.name)) and x.defining_class == obj]
                attrs.sort(cmp=lambda a, b: cmp(a.name.upper().replace("__INIT__", "A"*10), b.name.upper().replace("__INIT__", "A"*10)))
                if len(attrs) != 0:
                    contents += "\nMethods\n"
                    contents += "#######\n\n"

                for attr in attrs:
                    method = getattr(obj, attr.name)
                    name = attr.name

                    if not method.__doc__ and name in parsed.ignore:
                        continue

                    if "%s::%s" % (obj.__name__, name) in parsed.ignore:
                        continue

                    clnum += 1
                    this_toc += "%s. `%s::%s`_.\n" % (clnum, obj.__name__, name)
                    this_contents += "\n.. _%s::%s:\n\n" % (obj.__name__, name)
                    this_contents += "**%s::%s** " % (obj.__name__, name)
                    this_contents += inspect.formatargspec(*inspect.getargspec(method)).replace("*", "\*") + "\n"
                    if method.__doc__:
                        this_contents += "\n" + inspect.getdoc(method) + "\n"
                    else:
                        this_contents += "\n*Method undocumented*.\n"
                    this_contents += divider
                contents += this_toc
                contents += divider
                contents += this_contents
            else:
                contents += divider

    print toc, "\n", contents.rstrip(divider)

if __name__=="__main__":
    main()
