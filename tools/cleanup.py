#!/usr/bin/python3

from fontParts.world import *
import sys

# Open UFO
ufo = sys.argv[1]
font = OpenFont(ufo)

# Modify UFO
dottedcircle = font['dottedcircle']
dottedcircle.width = 0

# Save UFO
font.changed()
font.save()
font.close()
