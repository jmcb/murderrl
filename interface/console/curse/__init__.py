#!/usr/bin/env python

try:
    from _curse import *
except:
    put, get, clear, init, deinit = [lambda *a: None] * 5
