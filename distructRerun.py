#!/usr/bin/env python3

from distructComline import ComLine
from distruct import Distruct
from clumpp import Clumpp
from DefaultListOrderedDict import DefaultListOrderedDict
from pathlib import Path

import json
import os
import pandas
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

def createList(r1, r2):
	if( r1 == r2 ):
		return r1
	else:
		res = []
		while(r1 < r2+1 ):
			res.append(r1)
			r1 += 1
		return res

def qfileSort(qfilesDict):
	for k in qfilesDict.keys():
		# create initial list of columns that need to be sorted
		ncols = 4+int(k)
		colList = createList(5, ncols)
		#print(colList)
		
		# read qfile into dataframe
		df = pandas.read_csv(qfilesDict[k], delim_whitespace=True, header=None)

		# create list of values telling whether or not to sort ascending
		ascList = list() # hold value indicating whether sort will be ascending for each column
		colDict = dict() # hold dict of key=column, val=sum(column)
		for item in colList:
			colDict[item] = df[item].sum()
			#print(colDict[item])
			ascList.append(True)

		# get groups (k values) in order of least ancestry to greatest
		colSorted = dict(sorted(colDict.items(), key=lambda x:x[1], reverse=True))
		newlist = list()
		for key, value in colSorted.items():
			newlist.append(key)

		# conduct sorting by qvalue columns
		df.sort_values(by = newlist, ascending=ascList, ignore_index=True, inplace=True)

		# write to file - this overwrites input files in best_
		df.to_csv(qfilesDict[k], sep=' ', header=False, index=False)

def main():
	input = ComLine(sys.argv[1:])

	# The next six lines remove files to prevent duplication of data if distructRerun is executed multiple times on the same files.
	cvpath = Path("cv_file.MajClust.txt")
	llpath = Path("loglikelihood_file.MajClust.txt")
	if cvpath.is_file():
		os.remove(cvpath)
	if llpath.is_file():
		os.remove(llpath)
	
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

		# code to get CV and Loglikelihood values for major clusters must only be run once.
		if(k == int(input.args.maxk)):
			c.getMajorClusterCVvalues(input.args.majc)
			c.getMajorClusterLoglikelihood(input.args.majc)
		# code to get values for minor clusters operates on individual K values
		c.getMinorClusterCVvalues()
		c.getMinorClusterLoglikelihood()

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

	# add file sorting here

	# run distruct if option is used
	if input.args.run==True:
		d.runDistruct()

	# sort indivq files by q values if -s/--sort option is used
	if input.args.sort==True:
		qfileSort(qfilesDict)
		

# run main function
main()

raise SystemExit
