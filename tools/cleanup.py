#!/usr/bin/python3

from fontParts.world import *
import sys

# Open UFO
ufo = sys.argv[1]
font = OpenFont(ufo)

# Modify UFO

# we don't want to see the dottedcircle
# to work around an issue with shaping engines
dottedcircle = font['dottedcircle']
dottedcircle.width = 0

# candrabindu is a zero width mark
candrabindu = font['candrabindu']
width = candrabindu.width
candrabindu.leftMargin = -width
candrabindu.width = 0

# Save UFO
font.changed()
font.save()
font.close()
