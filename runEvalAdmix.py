#!/usr/bin/env python3

from evalAdmixComline import ComLine
from evaladmix import EvalAdmix
from plink import Plink

import sys

def main():
	input = ComLine(sys.argv[1:])

	# make plink .bed file and fix .fam file
	pl = Plink(input.args.prefix)
	pl.makeBED()
	pl.fixFam(input.args.popmap)

	ea = EvalAdmix(input.args.prefix)
	ea.evalAdmix(input.args.testK, input.args.np)
	ea.Rcode(input.args.evalAdmixRcode, input.args.testK)

main()

raise SystemExit
