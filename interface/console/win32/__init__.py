#!/usr/bin/env python

try:
    from _win32 import *
except:
    put, get, clear, init, deinit = [lambda *a: None] * 5
