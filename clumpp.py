from __future__ import print_function

from shutil import copyfile

import os

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

	def getMinorClusterRuns(self):
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

	def getCVvalues(self, mc):
		with open(mc) as mcruns:
			mcfiles = mcruns.readlines()
		with open("cv_file.txt", 'a') as cvf:
			for f in mcfiles:
				filepath = os.path.join(self.ad, f).rstrip()
				#print(filepath)
				with open(filepath, 'r') as cvin:
					for line in cvin.readlines():
						if 'CV' in line:
							cvf.write(line)

	def getMinorClusterCVvalues(self):
		print("test")

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
