#!/usr/bin/python3

from nameslist import *
import sys


with open(sys.argv[1], 'w') as output:
    for section in (vowels, matras, consonants, digits):
        chars = list()
        for char in section:
            chars.append(char)
        line = ''.join(chars) + '\n'
        output.write(line)
