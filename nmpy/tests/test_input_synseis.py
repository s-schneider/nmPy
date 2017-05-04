# Trial for a testing script, to make sure, the input files are correct
# for mdcplmrho methods.
#
# Simon Schneider, 2017

import numpy
import sys

infile = str(sys.argv[1])

def test_input_synseis(input):
    ifile = [line.strip() for line in open(input)]

    # Check for meaning of first integer, whats the link between this number and
    # the modes?
    if int(ifile[0]) > len(ifile):
        raise IOError('Wrong number of coupled modes in input file')

    for i,line in enumerate(ifile[1:]):
        if len(line) != 8:
            raise IOError('Wrong format of modes %s, specified in line %i, must have length of 8' % (line, i+1) )

        elements = line.split()
        if len(elements[0]) != 3:
            raise IOError('Wrong format of modes %s, specified in line %i, must be 3 digits' % (line, i+1) )

        if len(elements[2]) !=2:
            raise IOError('Wrong format of modes %s, specified in line %i, must be 2 digits' % (line, i+1) )

        if elements[1].islower():
            raise IOError('Wrong format of modes %s, specified in line %i, must be upper case' % (line, i+1) )

    print('Input file %s is correct' % input)

test_input_synseis(infile)
