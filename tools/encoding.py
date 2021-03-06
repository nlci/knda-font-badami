#!/usr/bin/python3

from fontParts.world import *
import sys

# Open UFO
ufo = sys.argv[1]
font = OpenFont(ufo)

# Modify UFO
ematra = font['ematra']
for contour in ematra.contours:
    if len(contour) <= 2:
        ematra.removeContour(contour)

# Save UFO
font.changed()
font.save()
font.close()
