#!/usr/bin/env python

"""
unit test for manor building.
"""

import sys
from builder import builder

if __name__=="__main__":
    if sys.argv[0] == "python":
        del sys.argv[0]

    del sys.argv[0]

    if len(sys.argv) == 0:
        sys.argv.append(2)
    if len(sys.argv) == 1:
        sys.argv.append(2)


    print builder.build_L(rooms=int(sys.argv[0]), rooms_wide=int(sys.argv[1])).combine()
