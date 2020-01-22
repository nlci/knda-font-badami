#!/usr/bin/python3

from nameslist import *
import sys


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

    output.write('Table\n')
    for c in consonants:
        conjuncts = list()
        for m in matras:
            conjuncts.append(c + m + n)
        line = ' '.join(conjuncts) + '\n'
        output.write(line)
