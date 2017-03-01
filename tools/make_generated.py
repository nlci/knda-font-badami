#!/usr/bin/python3

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("output", help="output file")
parser.add_argument("--version", action="version", version="%(prog)s 0.1")
args = parser.parse_args()

def main():
    Generate.generate(args.output)

class Generate(object):

    def __init__(self):
        pass

    @staticmethod
    def generate(filename):
        """Output generated test data"""

        ignore = (0x0C84, 0x0C8D, 0x0C91, 0x0CA9, 0x0CB4, 0x0CBA, 0x0CBB, 0x0CC5, 0x0CC9)
        output = open(filename, 'w')
        ka = chr(0x0C95)
        virama = chr(0x0CCD)
        for c1 in range(0x0C95, 0x0CB9):
            if not c1 in ignore:
                for c2 in range(0x0C95, 0x0CB9):
                    if not c2 in ignore:
                        output.write(ka + virama + chr(c1) + virama + chr(c2) + ' ')
                output.write('\n')

if __name__ == "__main__":
    main()
