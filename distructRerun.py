#!/usr/bin/env python3

from distructComline import ComLine
from distruct import Distruct
from clumpp import Clumpp
from DefaultListOrderedDict import DefaultListOrderedDict

import json
import os
import sys

def mergeDicts(dict1, dict2):
	newDict = {**dict1, **dict2}
	return newDict

def locationsDict(qd, iq, k):
	tempDict = dict()
	cd = os.getcwd()
	path = os.path.join(cd, qd, iq)
	tempDict[k] = path
	return tempDict

def jsonDump(admixDir, outfile, outputDict):
	outPath = os.path.join(admixDir, outfile)
	with open(outPath, 'w') as jf:
		json.dump(outputDict, jf, indent=4)

def main():
	input = ComLine(sys.argv[1:])
	
	d = Distruct(input.args.directory, input.args.otl, input.args.colorbrew, input.args.pathtocolorbrew)
	runsDict = DefaultListOrderedDict()
	qfilesDict = dict()
	for k in range(int(input.args.mink),int(input.args.maxk)+1):
		drawp = "drawparams." + str(k)
		outfile = "K" + str(k) + ".ps"

		c = Clumpp(input.args.directory, str(k), input.args.ad)
		popq,indivq,qdir = c.copyMajClustFiles() #return popq file, indivq file, and destination dir

		#record new locations of Q files for major clusters
		tempMajQfilesDict = locationsDict(qdir, indivq, str(k)) # record path to indivq for k
		qfilesDict = mergeDicts(qfilesDict, tempMajQfilesDict)

		popqList,indivqList = c.copyMinClustFiles()

		tempMajDict = c.getMajorClusterRuns(input.args.majc)
		runsDict = mergeDicts(runsDict, tempMajDict)

		tempMinDict = c.getMinorClusterRuns()
		runsDict = mergeDicts(runsDict, tempMinDict)
		
		#record new locations of Q files for minor clusters
		minClustKeys = list(tempMinDict.keys())#get keys from tempMinDict
		tempMinQfilesDict = dict(zip(minClustKeys, indivqList))
		for key, v in tempMinQfilesDict.items():
			tempDict = locationsDict(qdir, v, key)
			qfilesDict = mergeDicts(qfilesDict, tempDict)
		
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

	jsonDump(input.args.ad, "cvRuns.json", runsDict)
	jsonDump(input.args.ad, "qfilePaths.json", qfilesDict)

	if input.args.run==True:
		d.runDistruct()
	

main()

raise SystemExit
