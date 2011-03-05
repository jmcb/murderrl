#!/usr/bin/env python
"""
This is a series of decorators that will hopefully make automatically generated
documentation slightly more comprehensive.
"""

from functools import wraps

def extends (function_extending):
    """
    This is a documentation- and signature- preserving decorator. It takes the
    name of the function being "extended", and returns a wrapper which stores
    this information in the wrapped function. It uses functools.wraps in order
    to ensure consistency of documentation from the original function, while
    storing information about both in order to have this available to Sphinx
    and other documentation-generatnig programs.

    Primary use is::

        class Main (object):
            def __init__ (self, main1, main2, main3):
                pass

        class SubMain (Main):
            @extends(Main.__init__)
            def __init__ (self, *args, **kwargs):
                super(SubMain, self).__init__(*args, **kwargs)
                # Do something else here

    This allows the documentation to see that, while we have only defined
    variable arguments for SubMain.__init__, it is simply a wrapper that calls
    the aforementioned Main.__init__ function, and does a few extra things; as
    the signatures do not change, it makes no sense for the documentation to
    present the signature of SubMain.__init__ as ``(*args, **kwargs)``.

    :param function_extending: This is passed in to the decorator function and
      is stored as the ``extends`` member of the returned function. This should
      be the function that is "extended" by the decorated function.
    """
    def do_extension (function):
        if hasattr(function, "original"):
            original = function.original
        else:
            original = function

        @wraps (function)
        def wrapper (*args, **kwargs):
            function(*args, **kwargs)

        wrapper.extends = function_extending
        wrapper.original = original
        return wrapper

    return do_extension
