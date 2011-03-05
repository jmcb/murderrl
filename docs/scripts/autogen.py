#!/usr/bin/env python
import sys
sys.path.append("../")
from jinja2 import FileSystemLoader, Environment
import sphinx.ext.autosummary.generate

def main ():
    sphinx.ext.autosummary.generate.env = Environment(loader=FileSystemLoader('.templates'))
    sphinx.ext.autosummary.generate.main(argv=sys.argv)

if __name__=="__main__":
    main ()
