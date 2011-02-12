#!/usr/bin/env python

import random

##################################################
# Utility methods
def coinflip ():
    """
    Returns True with a 50% chance, else False.
    """
    return (random.randint(1,2) == 1)

def one_chance_in (n):
    """
    Returns True with a 1/n chance.
    """
    return (random.randint(1,n) == 1)
