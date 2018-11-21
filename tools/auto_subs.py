#!/usr/bin/python3

from nameslist import *
import sys


ka = consonants[0]
with open(sys.argv[1], 'w') as output:
    output.write('RenderingUnknown\n')
    for c1 in consonants:
        conjuncts = list()
        for c2 in consonants:
            conjuncts.append(ka + h + c1 + h + c2)
        line = ' '.join(conjuncts) + '\n'
        output.write(line)
