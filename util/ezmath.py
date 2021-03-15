#!/usr/bin/env micropython

def clamp(value, min, max):
    return max(min(value, max), min)
