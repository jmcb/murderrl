#!/usr/bin/env python
"""
unit test for manor building.
"""

from builder import manor

if __name__=="__main__":

    import sys
    type = ""
    if len(sys.argv) > 1:
        type = sys.argv[1].upper()

    if type == 'L':
        m = manor.build_L()
    elif type == 'Z':
        m = manor.build_Z()
    elif type == 'N':
        m = manor.build_N()
    elif type == 'H':
        m = manor.build_H()
    elif type == 'O':
        m = manor.build_O()
    else:
        m = manor.base_builder()

    print m.combine()
