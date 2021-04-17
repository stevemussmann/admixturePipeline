#!/usr/bin/env python3

from distructComline import ComLine
from distruct import Distruct
from clumpp import Clumpp
from DefaultListOrderedDict import DefaultListOrderedDict

import json
import sys

def mergeDicts(dict1, dict2):
	newDict = {**dict1, **dict2}
	return newDict

def main():
	input = ComLine(sys.argv[1:])
	
	d = Distruct(input.args.directory, input.args.otl, input.args.colorbrew, input.args.pathtocolorbrew)
	runsDict = DefaultListOrderedDict()
	for k in range(int(input.args.mink),int(input.args.maxk)+1):
		drawp = "drawparams." + str(k)
		outfile = "K" + str(k) + ".ps"

		c = Clumpp(input.args.directory, str(k), input.args.ad)
		popq,indivq = c.copyMajClustFiles()
		popqList,indivqList = c.copyMinClustFiles()

		tempMajDict = c.getMajorClusterRuns(input.args.majc)
		runsDict = mergeDicts(runsDict, tempMajDict)

		tempMinDict = c.getMinorClusterRuns()
		runsDict = mergeDicts(runsDict, tempMinDict)
		
		if(k == int(input.args.maxk)):
			c.getMajorClusterCVvalues(input.args.majc)
		c.getMinorClusterCVvalues()

		d.copyFiles()

		#drawparams for major clusters
		d.writeDrawparams(drawp, popq, indivq, str(k), outfile, c.pops, c.inds, input.args.width)

		#drawparams for minor clusters
		for pq, iq in zip(popqList, indivqList):
			temp = pq.split(".")
			drawpMinC = drawp + "." + temp[-1]
			outfileMinC = "K" + str(k) + "." + temp[-1] + ".ps"
			d.writeDrawparams(drawpMinC, pq, iq, str(k), outfileMinC, c.pops, c.inds, input.args.width)

	print(runsDict)
	with open("cvRuns.json", 'w') as jf:
		json.dump(runsDict, jf, indent=4)

	if input.args.run==True:
		d.runDistruct()
	

main()

raise SystemExit
