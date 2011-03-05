#!/usr/bin/env python

import sys
sys.path.append("../")

from sphinx.ext.autosummary.generate import *
env = Environment(loader=PackageLoader('sphinx.ext.autosummary', '.templates'))

main(argv=sys.argv)
