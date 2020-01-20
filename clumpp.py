from __future__ import print_function

from shutil import copyfile

import os

class Clumpp():
	'Class for finding and preparing clumpp output from the output produced by clumpak'

	def __init__(self,wd,k):
		self.wd = wd
		self.k = k

		#Construct path to where files should reside
		tempdir = "K=" + self.k
		self.mcdir = os.path.join(self.wd, tempdir, "MajorCluster")
		self.clusdir = os.path.join(self.mcdir,"clusterFiles")
		self.cdir = os.path.join(self.mcdir, "CLUMPP.files")

		# check to see if directory exists
		self.dirExists(self.cdir)

		self.oldind = "ClumppIndFile.output"
		self.oldpop = "ClumppPopFile"

		#Get the files that contain clumpp output
		self.clumppoutind = os.path.join(self.cdir, self.oldind)
		self.clumppoutpop = os.path.join(self.cdir, self.oldpop)

		#Check if files exist
		self.fileExists(self.clumppoutind)
		self.fileExists(self.clumppoutpop)

		#find number of individuals and populations
		self.inds = self.linecount(self.clumppoutind)
		self.pops = self.linecount(self.clumppoutpop)

	def getMajorClusterRuns(self,mc):
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

	def copyFiles(self):
		nd = self.makeDir()

		np = self.oldpop + "." + self.k
		newpop = os.path.join(nd, np)

		ni = self.oldind + "." + self.k
		newind = os.path.join(nd, ni)

		copyfile(self.clumppoutind, newind)
		copyfile(self.clumppoutpop, newpop)

		return np,ni

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
