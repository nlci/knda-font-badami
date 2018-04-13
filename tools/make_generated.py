#!/usr/bin/python3

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("output", help="output file")
parser.add_argument("--version", action="version", version="%(prog)s 0.2")
args = parser.parse_args()

def main():
    Generate.generate(args.output)

class Generate(object):

    def __init__(self):
        pass

    @staticmethod
    def generate(filename):
        """Output generated test data"""

        consonants = [
            0x0C95,  # KANNADA LETTER KA
            0x0C96,  # KANNADA LETTER KHA
            0x0C97,  # KANNADA LETTER GA
            0x0C98,  # KANNADA LETTER GHA
            0x0C99,  # KANNADA LETTER NGA
            0x0C9A,  # KANNADA LETTER CA
            0x0C9B,  # KANNADA LETTER CHA
            0x0C9C,  # KANNADA LETTER JA
            0x0C9D,  # KANNADA LETTER JHA
            0x0C9E,  # KANNADA LETTER NYA
            0x0C9F,  # KANNADA LETTER TTA
            0x0CA0,  # KANNADA LETTER TTHA
            0x0CA1,  # KANNADA LETTER DDA
            0x0CA2,  # KANNADA LETTER DDHA
            0x0CA3,  # KANNADA LETTER NNA
            0x0CA4,  # KANNADA LETTER TA
            0x0CA5,  # KANNADA LETTER THA
            0x0CA6,  # KANNADA LETTER DA
            0x0CA7,  # KANNADA LETTER DHA
            0x0CA8,  # KANNADA LETTER NA
            0x0CAA,  # KANNADA LETTER PA
            0x0CAB,  # KANNADA LETTER PHA
            0x0CAC,  # KANNADA LETTER BA
            0x0CAD,  # KANNADA LETTER BHA
            0x0CAE,  # KANNADA LETTER MA
            0x0CAF,  # KANNADA LETTER YA
            0x0CB0,  # KANNADA LETTER RA
            0x0CB1,  # KANNADA LETTER RRA
            0x0CB2,  # KANNADA LETTER LA
            0x0CB3,  # KANNADA LETTER LLA
            0x0CDE,  # KANNADA LETTER FA
            0x0CB5,  # KANNADA LETTER VA
            0x0CB6,  # KANNADA LETTER SHA
            0x0CB7,  # KANNADA LETTER SSA
            0x0CB8,  # KANNADA LETTER SA
            0x0CB9,  # KANNADA LETTER HA
            ]
        virama = chr(0x0CCD)
        ka = chr(consonants[0])
        with open(filename, 'w') as output:
            for c1 in consonants:
                conjuncts = list()
                for c2 in consonants:
                    conjuncts.append(ka + virama + chr(c1) + virama + chr(c2))
                line = ' '.join(conjuncts) + '\n'
                output.write(line)

if __name__ == "__main__":
    main()
