#!/usr/bin/env python
"""
docparser, a quick parser for documentation configuration.

This converts a flat representation of what methods and classes of what modules
should be documented, and in which sections, from text into an iterable
document. The file format for \*.conf files allows combinations of the following
signifiers:

:`$ignore`_: ``qualified name``
:`$search`_: ``path1``, ``path2``, ...
:`$module`_: ``module identifier``, ``module description``
:`$suppress`_: ``suppression target`` [1]_
:`$section`_: ``section description`` [2]_
:`$classes`_: ``class1``, ``class2``, ... [3]_
:`$methods`_:  ``method1``, ``method2``, ... [3]_
:``#``: ``comment text`` [4]_

.. [1] Suppression targets are defined per-module, thus must be included in a
       block of module definitions.
.. [2] Section sigifiers are associated with the most recent module signifier.
       If there is no previous module, they are discarded.
.. [3] Lists of classes and methods are associated with sections, and if there is no
       previous section signifier, they are discarded.
.. [4] Comments are simply ignored by the parser. Any line beginning with the
       ``#`` symbol will be skipped during parsing.

.. _$ignore:

``$ignore``
-----------

Arguments:

:``qualified name``: A string in the format of *function name* or *class
                     name::function name*.

``$ignore`` has two specific behaviours. If passed a non-qualified function
name, this function will be ignored when iterating over class members *if and
only if* the method is undocumented.

If passed a qualified class function name, this function will always be ignored.

*Examples*:

``$ignore __repr__``: All undocumented ``__repr__`` methods will be suppressed
from display.

``$ignore Document::__init__``: The ``__init__`` method of the ``Document``
class will be suppressed from display, regardless of whether or not it has been
documented.

All ``$ignore`` signifiers must be followed by a single string. To denote
multiple functions or methods to be ignored, use multiple ``$ignore``
signifiers, each with its own line.

.. _$search:

``$search``:
------------

Arguments: 

:[``path1``, ``path2``, ...]: A string of comma-separated search paths.

``$search`` allows you to specify additional paths that should be searched when
importing modules. These can be absolute paths of relative directories, but they
must each exist.

If ``$search`` is provided, it should be the first line of the document,
otherwise the actual parser will fail to properly import modules.

.. _$module:

``$module``
-----------

Arguments:

:``module identifier``: Must be a valid Python module identifier, and located in
                        the path. Must be unique.
:``module description``: A short string description of the module. Used for
                         generating module headers.

Definine a ``$module`` begins a new module block. If a module block has already
been begun, that module is closed and the result appended to the document's
module list. Defining a module allows for the definition of sections.

.. _$suppress:

``$suppress``
-------------

Arguments:

:``suppression target``: One of: "toc".

Currently, this only supports the suppression of, per-module, generating a table
of contents.

.. _$section:

``$section``
------------

Arguments:

:``section description``: A string used for section headlines. Must be unique.

Sections denote the beginning of a new block. If a previous section has been
defined, that section will be closed and appended to the current module. To
specify classes and modules that are to be documented, they must be associated
with a specific section.

.. _$classes:

``$classes``
------------

Arguments:

:[``class1``, ``class2``, ``...``]: A list of comma separated classes to be
                                    recursively documented. [3]_

.. _$methods:

``$methods``
------------

Arguments:

:[``method1``, ``method2``, ``...``]: A list of comma separated methods to be
                                      documented. [3]_

"""
import sys, os, inspect

class Document:
    """
    Defines an iterable list of modules and ignore targets.

    Members
    #######

    :``modules``: A list of ``Module`` relevant to this document.
    :``ignore``: A list of ignore targets relevant to this document.
    """
    modules = []
    ignore = []
    search_paths = []
    def __iter__ (self):
        """
        Yields a tuple of three values: ``module``, ``section`` and ``object``.
        Some or all of these may be ``None``. Specifically, iteration begins by
        yielding (``Module``, ``None``, ``None``)``; it then steps into the
        module and yields (``Module``, ``Section``, ``None``); it then steps
        into the section and yields (``Module``, ``Section``, ``Obj``) for each
        class and method the section defines, if any; finally, once it has
        reached the bottom of any tree, it steps back a level (from objects to
        sections, for instance) and tries the next tree; if there is no next
        tree, it steps back again, until finally all modules, their sections,
        and subsequent class or method lists have been exhausted.
        """
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
        """
        Provides a tree-like representation of the document.
        """
        result = "Document:\n"
        for module, section, obj in self:
            if section is None and obj is None:
                result += " -%s\n" % module.name
                x = False
            elif section is not None and obj is None:
                if len(section.classes) != 0:
                    result += "  -%s (classes)\n" % section.name
                x = True
            else:
                if inspect.isfunction(obj) and x == True and len(section.methods) != 0:
                    result += "  -%s (methods)\n" % section.name
                    x = False
                result += "   -%s\n" % obj.__name__
        return result

class Module:
    """
    Stores information about a Python module to be documented.

    Members
    #######

    :``sections``: A list of ``Sections`` relevant to this module.
    """
    module = None
    name = None
    sections = None
    identifier = None
    suppress_toc = False
    def __init__ (self, name=None):
        self.name = name
        self.module = None
        self.identifier = None
        self.sections = []
    def __repr__ (self):
        return "<Module name=%s>" % self.name
    def __eq__ (self, other):
        return isinstance(other, Module) and self.module == other.module
    def __ne__ (self, other):
        return isinstance(other, Module) and self.module != other.module

class Section:
    """
    Stores information about a section of a Python module to be documented.

    Members
    #######

    :``classes``: A list of strings of classes defined by the module.
    :``methods``: A list of strings of methods defined by the module.
    """
    name = None
    classes = None
    methods = None
    def __init__ (self, name=None):
        self.name = name
        self.classes = []
        self.methods = []
    def __repr__ (self):
        return "<Section name=%s, classes=%s, methods=%s>" % (self.name, self.classes, self.methods)
    def __eq__ (self, other):
        return isinstance(other, Section) and self.name == other.name
    def __ne__ (self, other):
        return isinstance(other, Section) and self.name == other.name

def docparser (filename, verbose=False):
    """
    Iterators over the provided filename, parses it, and returns a ``Document``.

    :``filename``: The filename to iterate over. Can either be a: ``file``
                   instance; a list of strings; a single, new line separated
                   string; or a string representing a file name.
    :``verbose``: If True, will provide parse-time messages about encountered
                  signifiers, etc. *Default False*.
    """
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
        if line.startswith("#"):
            continue

        if line.startswith("$module"):
            if cur_section is not None and cur_section not in cur_module.sections:
                cur_module.sections.append(cur_section)
                cur_section = None
            if cur_module is not None and cur_module not in doc.modules:
                doc.modules.append(cur_module)
                cur_module = None
            cur_module = Module()
            identifier, name = line.split(" ", 1)[1].split(", ")
            cur_module.module = __import__(identifier)
            cur_module.name = name
            cur_module.identifier = identifier
            if verbose:
                print cur_module
        if line.startswith("$suppress"):
            # Currently only allows suppresion of the TOC
            cur_module.suppress_toc = True
        elif line.startswith("$section"):
            if cur_section is not None and cur_section not in cur_module.sections:
                cur_module.sections.append(cur_section)
                cur_section = None
            cur_section = Section()
            cur_section.name = line.split(" ", 1)[1]
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
        elif line.startswith("$search"):
            paths = line.split(" ", 1)[1].split(", ")
            for path in paths:
                if verbose:
                    print "<SearchPath %s>" % path
                assert os.path.exists(path)
                doc.search_paths.append(path)
                sys.path.append(path)
        else:
            if verbose:
                print "Unknown symbol: " + line

    if cur_section is not None and cur_section not in cur_module.sections:
        cur_module.sections.append(cur_section)

    if cur_module is not None and cur_module not in doc.modules:
        doc.modules.append(cur_module)

    return doc

