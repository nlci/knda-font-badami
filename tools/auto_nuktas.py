#!/usr/bin/python3

import sys
from nameslist import *


def process(chars, label, output):
    output.write(label + '\n')
    conjuncts = list()
    for c in chars:
        conjuncts.append(c + n)
    line = ' '.join(conjuncts) + '\n'
    output.write(line)


with open(sys.argv[1], 'w') as output:
    output.write('RenderingUnknown\n')
    process(vowels, 'Vowels', output)
    process(consonants, 'Consonants', output)
    process(akhands, 'Akhands', output)
