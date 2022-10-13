#!/usr/bin/python3

from fontParts.world import *
import sys

# Open UFO
ufo = sys.argv[1]
font = OpenFont(ufo)

# Modify UFO

# ssa.sub RSB way too much to the left in Badami
if font.info.familyName == 'Badami':
    source = font['pha.sub']
    target = font['ssa.sub']
    target.rightMargin = source.rightMargin

# make candrabindu from the om sign
spacingcandrabindu = font['spacingcandrabindu']
spacingcandrabindu.decompose()
for contour in spacingcandrabindu.contours:
    if len(contour) > 10:
        spacingcandrabindu.removeContour(contour)

# Save UFO
font.changed()
font.save()
font.close()
