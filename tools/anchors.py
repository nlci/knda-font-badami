#!/usr/bin/python3

from fontParts.world import *
from palaso.unicode.ucd import get_ucd
import sys

# Open UFO
ufo = sys.argv[1]
font = OpenFont(ufo)
print(f'Add anchors for {ufo}')

# Modify UFO

# Akhands
akhand1 = ('ka_ssa', 'ka_ssa.base', 'ka_ssa.imathra')
akhand2 = ('ja_nya', 'ja_nya.base', 'ja_nya.imathra')
akhands = akhand1 + akhand2

## Position nukta marks
nuktas = ('nukta', 'nukta.alt')
vedic_dots = ('vedictonetwodotsbelow', 'vedictonedotbelow')
for nukta, vedic_dot in zip(nuktas, vedic_dots):
    vg = font[vedic_dot]
    (xmin, ymin, xmax, ymax) = vg.bounds
    xcenter = (xmin + xmax) / 2
    ycenter = (ymin + ymax) / 2
    # The nukta glyphs are references
    # so the calculations were done on the source glyphs.
    ng = font[nukta]
    ng.appendAnchor('_N', (xcenter, ycenter))

## Position ematra...

#ematra = font['ematra']
#(xmin, ymin, xmax, ymax) = ematra.bounds
#ematra.appendAnchor('_V', (xmax, ymin))

jha_base = font['jha.base']
for anchor in jha_base.anchors:
    if anchor.name == 'V':
        x = anchor.x
        y = anchor.y
        jha_regbase = font['jha.regbase']
        jha_regbase.appendAnchor('V', (x, y))

## Position both
for glyph in font:
    bounds = glyph.bounds
    if bounds is None:
        continue
    (xmin, ymin, xmax, ymax) = bounds
    xcenter = (xmin + xmax) / 2

    # ...on some consonants.
    #if glyph.name in ('jha.base', 'ma.base', 'ya.base'):
    #    glyph.appendAnchor('V', (xcenter, ymax + 50))

    # Position sub sub forms
    if (glyph.name.endswith('.sub') or
        glyph.name in ('ra.below', 'ra.below.large', 'ra.below.ra') + akhands):
        # Add anchors.
        glyph.appendAnchor('S', (xmax + 50, -200))
        if glyph.name.endswith('.sub'):
            glyph.appendAnchor('_S', (xmin, 0))

    # Position nuktas on bases
    character_name = ''
    if glyph.unicode:
        character_name = get_ucd(glyph.unicode, 'na')
    if character_name.startswith('KANNADA LETTER') or glyph.name in akhands:
        glyph.appendAnchor('N', (xcenter, ymin + ycenter))

    # Add un-used anchors on matras so they will be classified as marks in OpenType
    if glyph.name.endswith('matra') or glyph.name == 'lengthmark' or glyph.name.startswith('ra.below'):
        glyph.appendAnchor('_M', (0, 0))

# Save UFO
font.changed()
font.save()
font.close()
