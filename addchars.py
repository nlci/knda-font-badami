#!/usr/bin/python3

from addcharslib import *

for f in faces:

    workshop = 1.4
    upm2048 = 1000.0/2048.0
    upm1000 = 1.0
    scale2048 = str(upm2048/workshop)
    scale1000 = str(upm1000/workshop)

    lighter = {
        'Regular': 'Medium',
        'Italic': 'MediumItalic',
        'Bold': 'Demibold',
        'Bold Italic': 'DemiboldItalic'
        }
    heavier = {
        'Regular': 'Demibold',
        'Italic': 'DemiboldItalic',
        'Bold': 'Bold',
        'Bold Italic': 'BoldItalic'
        }

    for sn in stylesName:
        if f == 'Kaveri':
            # esn = lighter[sn]
            esn = heavier[sn]
            modifyFile(scale1000, 'exo', f, sn, esn)
            modifyFile(scale2048, 'charis', f, sn)
        else:
            modifyFile(scale2048, 'gentium', f, sn)
