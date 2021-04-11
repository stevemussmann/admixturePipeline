#!/usr/bin/env python3

from distructComline import ComLine
from distruct import Distruct
from clumpp import Clumpp

import sys

def main():
	input = ComLine(sys.argv[1:])

	for k in range(int(input.args.mink),int(input.args.maxk)+1):
		drawp = "drawparams." + str(k)
		outfile = "K" + str(k) + ".ps"

		c = Clumpp(input.args.directory, str(k), input.args.ad)
		popq,indivq = c.copyMajClustFiles()
		popqList,indivqList = c.copyMinClustFiles()

		c.getMajorClusterRuns(input.args.majc)
		c.getMinorClusterRuns()

		c.getMajorClusterCVvalues(input.args.majc)
		c.getMinorClusterCVvalues()

		d = Distruct(input.args.directory, input.args.otl, input.args.colorbrew, input.args.pathtocolorbrew)
		d.copyFiles()

		#drawparams for major clusters
		d.writeDrawparams(drawp, popq, indivq, str(k), outfile, c.pops, c.inds, input.args.width)

		#drawparams for minor clusters
		for pq, iq in zip(popqList, indivqList):
			temp = pq.split(".")
			drawpMinC = drawp + "." + temp[-1]
			outfileMinC = "K" + str(k) + "." + temp[-1] + ".ps"
			d.writeDrawparams(drawpMinC, pq, iq, str(k), outfileMinC, c.pops, c.inds, input.args.width)

		if input.args.run==True:
			d.runDistruct()

main()

raise SystemExit
