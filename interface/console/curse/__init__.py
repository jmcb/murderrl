#!/usr/bin/env python

UNAVAILABLE = False

try:
    from _curse import *
except:
    put, get, clear, init, deinit = [lambda *a: None] * 5
    UNAVAILABLE = True
