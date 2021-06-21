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

	ea = EvalAdmix(input.args.prefix, input.args.mc,input.args.evalAdmixRcode)
	ea.loadJson()
	ea.evalAdmix(input.args.minK, input.args.maxK, input.args.np)
	ea.Rcode(input.args.evalAdmixRcode, input.args.minK, input.args.maxK)

	ea.averageCorres(input.args.evalAdmixRcode)

main()

raise SystemExit
