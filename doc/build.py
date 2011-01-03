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
    identifier = None
    def __init__ (self, name=None):
        self.name = name
        self.module = None
        self.identifier = None
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
            if cur_module is not None and cur_module not in doc.modules:
                doc.modules.append(cur_module)
                cur_module = None
            cur_module = Module()
            cur_module.module = __import__(line.split(" ", 2)[1])
            cur_module.name = line.split(" ", 2)[2]
            cur_module.identifier = line.split(" ", 2)[1]
            if verbose:
                print cur_module
        elif line.startswith("$section"):
            if cur_section is not None and cur_section not in cur_module.sections:
                cur_module.sections.append(cur_section)
                cur_section = None
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

    if cur_module is not None and cur_module not in doc.modules:
        doc.modules.append(cur_module)

    return doc

#####################################################################
#####################################################################
# Actual doc generation goes from here down.

def main (args):
    build_all = False
    build_modules = False
    build_index = False

    if "modules" in args:
        build_all = False
        output = "%s.rst"
        build_modules = True
    else: #if "all" in args
        output = "index.rst"
        build_all = True
    if "index" in args:
        build_index = True
    else:
        build_index = False

    parsed = docparser("doc.conf")

    modules = []
    previous_module = None

    class Scope:
        num = 0
        snum = 0
        cnum = 0
        toc = ""
        contents = ""
        index = ""
        def __init__ (self):
            self.index = []

    s = Scope()

    def write_module ():
        open(output % previous_module, "w").write((s.toc + "\n" + s.contents.rstrip(divider)))

    def write_all ():
        open(output, "w").write((s.toc + "\n" + s.contents.rstrip(divider)))

    def close_module ():
        s.num = 0
        s.snum = 0
        s.cnum = 0
        s.toc = """\nTable of Contents\n=================\n"""
        s.contents = ""
        s.index = []

    def make_index ():
        s.toc += "\n%s. `Index`_" % (s.num+1)

        s.index.sort(cmp=lambda a, b: cmp(a.upper().replace("__INIT__", "A"*10), b.upper().replace("__INIT__", "A"*10)))
        side_a = s.index[0::2]
        a_size = sorted([len(x) for x in side_a], reverse=True)[0]
        side_b = s.index[1::2]
        b_size = sorted([len(x) for x in side_b], reverse=True)[0]

        total_size = a_size + b_size + 10
        column_size = total_size/2

        index_term = "`%s`_"

        def pad (term):
            while len(term) < column_size:
                term += " "
            return term

        table = "+" + "-" * (total_size/2) + "+" + "-" * (total_size/2) + "+\n"
        for terms in zip(side_a, side_b):
            for term in terms:
                table += "|" + pad(index_term % term)
            table += "|\n+" + "-" * (total_size/2) + "+" + "-" * (total_size/2) + "+\n"

        s.contents += "\n"
        s.contents += ".. _Index:\n"
        s.contents += "\n"
        s.contents += "Index\n"
        s.contents += "=====\n"
        s.contents += "\n"
        s.contents += table

    close_module()

    for module, section, obj in parsed:
        if section is None and obj is None:
            if build_modules and previous_module is not None:
                if build_index:
                    make_index()
                write_module()
                close_module()

            previous_module = module.identifier
            s.snum = 0
            s.num += 1
            s.toc += "\n"
            s.toc += ("%s. `"+module.name+"`_\n") % s.num
            s.contents += "\n.. _" +module.name+":\n\n"
            s.contents += module.name+"\n"
            s.contents += "=" * len(module.name)+"\n"
            if module.module.__doc__:
                s.contents += "\n" + inspect.getdoc(module.module) + "\n"
            s.contents += divider
        elif section is not None and obj is None:
            s.cnum = 0
            s.snum += 1
            s.toc += "\n"
            s.toc += ("  %s. `"+section.name+"`_\n\n") % chr(s.snum + 64)
            s.contents += "\n.. _"+section.name+":\n\n"
            s.contents += section.name+"\n"
            s.contents += "-" * len(section.name)+"\n"
            if len(section.classes) != 0:
                s.contents += "\nClasses\n#######\n"
                tree = inspect.getclasstree(section.classes)
                this_toc = "\n"
                for tier in tree[1]:
                    if isinstance(tier, list):
                        this_toc += "\n"
                        for subclass in tier:
                            this_toc += " - `%s`_.\n" % subclass[0].__name__
                        this_toc += "\n"
                    elif isinstance(tier, tuple):
                        this_toc += "- `%s`_.\n" % tier[0].__name__
                s.contents += this_toc
        elif obj is not None:
            s.cnum += 1
            cur_object = obj.__name__
            s.index.append(cur_object)
            s.toc += ("    %s. `"+cur_object+"`_\n") % chr(s.cnum + 96)
            s.contents += "\n.. _"+cur_object+":\n\n"
            if inspect.isclass(obj):
                desc = "class *%s*" % cur_object
            elif inspect.isfunction(obj):
                desc = "function *%s* %s" % (cur_object, inspect.formatargspec(*inspect.getargspec(obj)))
            else:
                desc = "*%s*" % cur_object
            s.contents += desc + "\n"
            s.contents += ("^" * len(desc)) +"\n"
            if obj.__doc__:
                s.contents += "\n" + inspect.getdoc(obj) + "\n"
            if inspect.isclass(obj):
                clnum = 0
                this_toc = ""
                this_contents = ""
                attrs = inspect.classify_class_attrs(obj)
                attrs = [x for x in attrs if x.kind == "method" and inspect.ismethod(getattr(obj, x.name)) and x.defining_class == obj]
                attrs.sort(cmp=lambda a, b: cmp(a.name.upper().replace("__INIT__", "A"*10), b.name.upper().replace("__INIT__", "A"*10)))
                if len(attrs) != 0:
                    s.contents += "\nMethods\n"
                    s.contents += "#######\n\n"

                for attr in attrs:
                    method = getattr(obj, attr.name)
                    name = attr.name
                    qname = "%s::%s" % (obj.__name__, name)

                    if not method.__doc__ and name in parsed.ignore:
                        continue

                    if qname in parsed.ignore:
                        continue

                    s.index.append(qname)

                    clnum += 1
                    this_toc += "%s. `%s`_.\n" % (clnum, qname)
                    this_contents += "\n.. _%s:\n\n" % qname
                    this_contents += "**%s** " % qname
                    this_contents += inspect.formatargspec(*inspect.getargspec(method)).replace("*", "\*") + "\n"
                    if method.__doc__:
                        this_contents += "\n" + inspect.getdoc(method) + "\n"
                    else:
                        this_contents += "\n*Method undocumented*.\n"
                    this_contents += divider
                s.contents += this_toc
                s.contents += divider
                s.contents += this_contents
            else:
                s.contents += divider

    if build_index:
        make_index()

    if build_modules and previous_module is not None:
        write_module()
        close_module()
    elif build_all:
        write_all()

if __name__=="__main__":
    main(sys.argv)
