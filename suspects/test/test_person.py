#!/usr/bin/env python
from suspects.person import *

def main (num = 10):
    """
    Generate a list of suspects and display them.

    :``num``: The number of suspects to be generated. *Default 10*.
    """
    sl = SuspectList(num)
    sl.print_suspects()

if __name__ == "__main__":
    """
    Generate a list of suspects and display them.

    :``max_suspects``: The number of suspects to be generated. *Default 10*.
    """
    import sys

    # As each letter can only be used once, there's a fixed cap
    # at 26 suspects, but seeing how some letters are really rare
    # (or have no names assigned) we should not try for more than
    # around 20.
    max_suspects = 10
    if len(sys.argv) > 1:
        try:
            max_suspects = min(int(sys.argv[1]), 20)
        except ValueError:
            sys.stderr.write("Warning: Expected integer argument, using default value %d\n" % max_suspects)
            pass

    main(max_suspects)
