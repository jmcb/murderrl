#!/usr/bin/env python
import sys

import auto

sys.path.append("..")

from jinja2 import FileSystemLoader
from jinja2.sandbox import SandboxedEnvironment

from sphinx.ext.autodoc import (ModuleDocumenter,ClassDocumenter,ExceptionDocumenter,DataDocumenter,FunctionDocumenter,MethodDocumenter,AttributeDocumenter,InstanceAttributeDocumenter)

from sphinx.ext.autodoc import AutoDirective, add_documenter

for typ in (ModuleDocumenter,ClassDocumenter,ExceptionDocumenter,DataDocumenter,FunctionDocumenter,MethodDocumenter,AttributeDocumenter,InstanceAttributeDocumenter):
    add_documenter(typ)

from sphinx.ext.autosummary import get_documenter

def main ():
    loader = FileSystemLoader([".templates"])
    env = SandboxedEnvironment(loader=loader)

    done_files = []

    for orig_module in auto.modules:
        output = orig_module + ".rst"

        f = open(output, "w")

        try:
            mod_base = orig_module.split(".")[-1]
            module = __import__(orig_module, fromlist=mod_base)

            def get_members (obj, typ):
                items = [
                    name for name in dir(obj)
                    if get_documenter(getattr(obj, name), obj).objtype == typ
                ]
                return items

            ns = {}
            ns['members'] = dir(module)
            ns['functions'] = get_members(module, 'function')
            ns['classes'] = get_members(module, 'class')
            ns['exceptions'] = get_members(module, 'exception')
            ns['name'] = mod_base
            ns['fullname'] = orig_module
            ns['name_underline'] = "=" * len(mod_base)
            ns['fullname_underline'] = "=" * len(orig_module)

            template = env.get_template("module.rst")
            rendered = template.render(**ns)
            f.write(rendered)
        finally:
            f.close()
            done_files.append(output)

    summary_template = open("summary.rst.template").read()
    modules = ""

    for module in done_files:
        modules += "    %s\n" % module

    f = open("summary.rst", "w")
    f.write(summary_template % {"files": modules})
    f.close()

if __name__=="__main__":
    main ()
