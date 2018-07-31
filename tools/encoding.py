#!/usr/bin/python3

from fontParts.world import *
import sys

# Open UFO
ufo = sys.argv[1]
font = OpenFont(ufo)

# Modify UFO
l = font['u0962']
ll = font['u0963']

l.name = 'lvocalicmatra'
ll.name = 'llvocalicmatra'

l.unicode = 0x0CE2
ll.unicode = 0x0CE3

# Save UFO
font.changed()
font.save()
font.close()
