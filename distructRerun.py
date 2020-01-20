#!/usr/bin/python

from distructComline import ComLine
from distruct import Distruct
from clumpp import Clumpp

import sys



def main():
	input = ComLine(sys.argv[1:])

	for k in xrange(int(input.args.mink),int(input.args.maxk)+1):
		drawp = "drawparams." + str(k)
		outfile = "K" + str(k) + ".ps"

		c = Clumpp(input.args.directory, str(k))
		popq,indivq = c.copyFiles()
		c.getMajorClusterRuns(input.args.mc)

		d = Distruct(input.args.directory, input.args.otl)
		d.copyFiles()
		d.writeDrawparams(drawp, popq, indivq, str(k), outfile, c.pops, c.inds)

main()

raise SystemExit
