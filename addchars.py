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
        'Italic': 'Medium Italic',
        'Bold': 'SemiBold',
        'Bold Italic': 'SemiBold Italic'
        }
    heavier = {
        'Regular': 'SemiBold',
        'Italic': 'SemiBold Italic',
        'Bold': 'Bold',
        'Bold Italic': 'Bold Italic'
        }

    for sn in stylesName:
        if f == 'Kaveri':
            # styles = lighter
            styles = heavier
            modifyFile(scale1000, 'exo', f, sn, styles)
            modifyFile(scale2048, 'andika', f, sn)
        else:
            styles = {
                'Regular': 'Medium',
                'Italic': 'Medium Italic',
            }
            modifyFile(scale2048, 'gentium', f, sn, styles)
