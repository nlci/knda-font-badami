#!/usr/bin/python3

from nameslist import *
import sys


with open(sys.argv[1], 'w') as output:
    output.write('RenderingUnknown\n')

    for c0 in (ka, ga, gha, ja):
        output.write(c0 + '\n')
        for c1 in consonants:
            conjuncts = list()
            for c2 in consonants:
                conjuncts.append(c0 + h + c1 + h + c2)
            line = ' '.join(conjuncts) + '\n'
            output.write(line)
