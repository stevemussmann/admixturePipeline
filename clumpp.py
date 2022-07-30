from __future__ import print_function

from shutil import copyfile
from DefaultListOrderedDict import DefaultListOrderedDict

import os
import sys

class Clumpp():
	'Class for finding and preparing clumpp output from the output produced by clumpak'

	def __init__(self,wd,k,ad):
		self.wd = wd
		self.k = k
		self.ad = ad

		#Construct path to where files should reside
		tempdir = "K=" + self.k
		self.kdir = os.path.join(self.wd, tempdir) 
		self.majcdir = os.path.join(self.kdir, "MajorCluster")
		self.clusdir = os.path.join(self.majcdir,"clusterFiles")
		self.cdir = os.path.join(self.majcdir, "CLUMPP.files")

		# check to see if major cluster directory exists
		self.dirExists(self.cdir)

		self.oldind = "ClumppIndFile.output"
		self.oldpop = "ClumppPopFile"

		#Get the files that contain clumpp output from major cluster directory
		self.clumppoutind = os.path.join(self.cdir, self.oldind)
		self.clumppoutpop = os.path.join(self.cdir, self.oldpop)

		#Check if major cluster files exist
		self.fileExists(self.clumppoutind)
		self.fileExists(self.clumppoutpop)

		#Check if minor clusters exist
		self.mincdir = list()
		dirContents = os.listdir(self.kdir)
		for d in dirContents:
			td = os.path.join(self.kdir, d)
			if os.path.isdir(td):
				if os.path.basename(td).startswith("MinorCluster"):
					self.mincdir.append(td)
		#print(self.mincdir)

		#Get the files that contain clumpp output from minor cluster directories
		self.minclumppoutind = list()
		self.minclumppoutpop = list()
		for d in self.mincdir:
			tdi = os.path.join(d, "CLUMPP.files", self.oldind)
			self.minclumppoutind.append(tdi)
			self.fileExists(tdi)

			tdp = os.path.join(d, "CLUMPP.files", self.oldpop)
			self.minclumppoutpop.append(tdp)
			self.fileExists(tdp)

		#find number of individuals and populations
		self.inds = self.linecount(self.clumppoutind)
		self.pops = self.linecount(self.clumppoutpop)

	def copyMajClustFiles(self):
		nd = self.makeDir()

		np = self.oldpop + "." + self.k
		newpop = os.path.join(nd, np)

		ni = self.oldind + "." + self.k
		newind = os.path.join(nd, ni)

		copyfile(self.clumppoutind, newind)
		copyfile(self.clumppoutpop, newpop)

		return np,ni,nd

	def copyMinClustFiles(self):
		nd = self.makeDir()
		npList = list()
		niList = list()

		for f in self.minclumppoutind:
			allLevels = self.splitAll(f)
			minClust = allLevels[-3]

			ni = self.oldind + "." + self.k + "." + minClust
			newind = os.path.join(nd, ni)

			niList.append(ni)

			copyfile(f, newind)

		for f in self.minclumppoutpop:
			allLevels = self.splitAll(f)
			minClust = allLevels[-3]
			
			np = self.oldpop + "." + self.k + "." + minClust
			newpop = os.path.join(nd, np)

			npList.append(np)

			copyfile(f, newpop)

		return npList,niList

	def getMinorClusterRuns(self):
		mcRunsDict = DefaultListOrderedDict() #dict of runs associated with K for json dump
		for d in self.mincdir:
			bn = os.path.basename(d)
			num = bn.replace("MinorCluster", "")
			fn = "MinorClusterRuns.K" + str(self.k) + "." + str(num)
			with open(fn, 'w') as mcruns:
				content = list()
				clusDir = os.path.join(d, "clusterFiles")
				with open(clusDir) as f:
					content = f.readlines()
				for line in content:
					tlist = line.split(".")
					tlist.pop(-1)
					tlist.pop(-1)
					tlist.append("stdout")
					temp = ".".join(tlist)
					mcruns.write(temp)
					mcruns.write("\n")
					newKey = str(self.k) + ".MinClust." + str(num) #make new key for minor cluster
					mcRunsDict[newKey].append(temp)
		return mcRunsDict

	def getMajorClusterRuns(self,mc):
		mcRunsDict = DefaultListOrderedDict() #dict of runs associated with K for json dump
		with open(mc, 'a') as mcruns:
			content = list()
			with open(self.clusdir) as f:
				content = f.readlines()
			for line in content:
				tlist = line.split(".")
				tlist.pop(-1)
				tlist.pop(-1)
				tlist.append("stdout")
				temp = ".".join(tlist)
				mcruns.write(temp)
				mcruns.write("\n")
				mcRunsDict[self.k].append(temp)
		return mcRunsDict

	def getMajorClusterLoglikelihood(self, mc):
		with open(mc) as mcruns:
			mcfiles = mcruns.readlines()
		with open("loglikelihood_file.MajClust.txt", 'a') as llf:
			for f in mcfiles:
				templist = f.split(".")
				templist2 = templist[-2].split("_")
				k=templist2[0]
				filepath = os.path.join(self.ad, f).rstrip()
				with open(filepath, 'r') as llin:
					for line in llin.readlines():
						if line.startswith('Loglikelihood'):
							llf.write(str(k))
							llf.write("\t")
							llf.write(line)
	
	def getMinorClusterLoglikelihood(self):
		match = "MinorClusterRuns.K" + str(self.k) + "."
		content = os.listdir(os.getcwd())
		for f in content:
			if f.startswith(match):
				with open(f) as mcruns:
					mcfiles = mcruns.readlines()
				temp = f.split(".")
				newlist = list()
				newlist.append("loglikelihood_file")
				newlist.append("MinClust")
				for item in temp[-2:]:
					newlist.append(item)
				newlist.append("txt")
				outfile = ".".join(newlist)
				with open(outfile, 'w') as llf:
					for f in mcfiles:
						filepath = os.path.join(self.ad, f).rstrip()
						with open(filepath, 'r') as llin:
							for line in llin.readlines():
								if line.startswith('Loglikelihood'):
									llf.write(str(self.k))
									llf.write("\t")
									llf.write(line)

	def getMajorClusterCVvalues(self, mc):
		with open(mc) as mcruns:
			mcfiles = mcruns.readlines()
		with open("cv_file.MajClust.txt", 'a') as cvf:
			for f in mcfiles:
				filepath = os.path.join(self.ad, f).rstrip()
				#print(filepath)
				with open(filepath, 'r') as cvin:
					for line in cvin.readlines():
						if 'CV' in line:
							cvf.write(line)

	def getMinorClusterCVvalues(self):
		match = "MinorClusterRuns.K" + str(self.k) + "."
		content = os.listdir(os.getcwd())
		for f in content:
			if f.startswith(match):
				with open(f) as mcruns:
					mcfiles = mcruns.readlines()
				temp = f.split(".")
				newlist = list()
				newlist.append("cv_file")
				newlist.append("MinClust")
				for item in temp[-2:]:
					newlist.append(item)
				newlist.append("txt")
				outfile = ".".join(newlist)
				with open(outfile, 'w') as cvf:
					for f in mcfiles:
						filepath = os.path.join(self.ad, f).rstrip()
						with open(filepath, 'r') as cvin:
							for line in cvin.readlines():
								if 'CV' in line:
									cvf.write(line)

	def makeDir(self):
		nd = os.path.join(self.wd, "best_results")
		if not os.path.exists(nd):
			os.makedirs(nd)
		return nd

	def linecount(self,fname):
		with open(fname) as f:
			for i, l in enumerate(f):
				pass
		return i+1

	def fileExists(self, filename):
		if( os.path.isfile(filename) != True ):
			print( filename, "does not exist" )
			print( "Exiting program..." )
			print( "" )
			raise SystemExit
		else:
			print(filename, "Exists")

	def dirExists(self,directory):
		if(os.path.isdir(directory) != True):
			print(repr(directory), "does not exist")
			print("Exiting program...")
			print("")
			raise SystemExit
		else:
			print(directory, "Exists")
	
	def splitAll(self,path):
		allparts = list()
		while 1:
			parts = os.path.split(path)
			if parts[0] == path:
				allparts.insert(0, parts[0])
				break
			elif parts[1] == path:
				allparts.insert(0, parts[1])
				break
			else:
				path = parts[0]
				allparts.insert(0, parts[1])
		return allparts
