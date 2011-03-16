#!/usr/bin/env python
"""
unit test for manor building.
"""

from builder import builder

if __name__=="__main__":

    import sys
    type = None
    if len(sys.argv) > 1:
        type = sys.argv[1].upper()

    m = builder.builder_by_type(type)

    print m.combine()
