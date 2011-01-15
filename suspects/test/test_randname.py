#!/usr/bin/env python
from suspects.randname import *

def generate_names (num = 10, style = None, gender = None):
    """
    Generates and outputs a given number of random names.

    :``num``: The number of repeats. *Default 10*.
    :``style``: One of ``'upper'``, ``'middle'``, ``'lower'`` for
                upper-, middle- and lowerclass names, respectively.
                *Default random*.
    :``gender``: Gender: ``'m'`` or ``'f'``. *Default random*.
    """

    check_name_db()

    for i in xrange(num):
        print get_random_fullname(gender, style)

if __name__ == "__main__":
    """
    Outputs a given amount of British names.

    :``num``: The number of repeats. *Default 10*.
    :``style``: One of ``'upper'``, ``'middle'`` or ``'lower'`` for
                upper-, middle- and lowerclass names, respectively.
                *Default random*.
    :``gender``: Gender: ``'m'`` or ``'f'``. *Default random*.
    """
    num    = 10
    style  = None
    gender = None

    if len(sys.argv) > 1:
        try:
            num = int(sys.argv[1])
        except ValueError:
            sys.stderr.write("Error: Expected integer argument, using default value %d\n" % num)
            pass
        if len(sys.argv) > 2:
            style = sys.argv[2]
            if len(sys.argv) > 3:
                gender = sys.argv[3]

    generate_names(num, style, gender)
