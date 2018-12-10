#!/usr/bin/python3

from nameslist import *
import sys


with open(sys.argv[1], 'w') as output:
    output.write('RenderingUnknown\n')

    for c0 in consonants:
        for c1 in consonants:
            for c2 in consonants:
                conjuncts = list()
                for m in [''] + matras:
                    conjuncts.append(c0 + h + c1 + h + c2 + m)
                line = ' '.join(conjuncts) + '\n'
                output.write(line)
