#!/usr/bin/env python

UNAVAILABLE = False

try:
    from _win32 import *
except:
    put, get, clear, init, deinit = [lambda *a: None] * 5
    UNAVAILABLE = True
