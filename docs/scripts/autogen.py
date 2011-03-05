#!/usr/bin/env python
import sys

import auto

sys.path.append("..")

from jinja2 import FileSystemLoader
from jinja2.sandbox import SandboxedEnvironment
from sphinx.ext.autosummary import get_documenter

def main ():
    loader = FileSystemLoader([".templates"])
    env = SandboxedEnvironment(loader=loader)

    for module in auto.modules:
        output = module + ".rst"

        f = open(output, "w")

        try:
            mod_base = module.split(".")[-1]
            module = __import__(module, fromlist=mod_base)

            def get_members (obj, typ):
                items = [
                    name for name in dir(obj)
                    if get_documenter(getattr(obj, name), obj).objtype == typ
                ]
                return items

            ns = {}
            ns['members'] = dir(module)
            ns['functions'], ns['all_functions'] = \
                               get_members(module, 'function')
            ns['classes'], ns['all_classes'] = \
                             get_members(module, 'class')
            ns['exceptions'], ns['all_exceptions'] = \
                               get_members(module, 'exception')

            template = env.get_template("module.rst")
            rendered = template.render(**ns)
            f.write(rendered)
        finally:
            f.close()

if __name__=="__main__":
    main ()
