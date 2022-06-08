#!/usr/bin/python3

from nameslist import *
import sys


with open(sys.argv[1], 'w') as output:
    output.write('RenderingUnknown\n')

    for c0 in (ka, ra):
        output.write(c0 + '\n')
        conjuncts = list()
        for wm in wrapmatras:
            conjuncts.append(c0 + h + c0 + wm)
            conjuncts.append(c0 + h + c0 + h + c0 + wm)
        line = ' '.join(conjuncts) + '\n'
        output.write(line)
