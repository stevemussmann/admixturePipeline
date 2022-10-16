from __future__ import print_function

from syscall import SysCall
from DefaultListOrderedDict import DefaultListOrderedDict

import argparse
import csv
import json
import os
import os.path
import shutil
import subprocess
import sys
import time
import numpy as np
import zipfile

class Admixture():
	'Class for executing Admixture commands'


	def __init__(self, prefix, NP, minK, maxK, rep, cv, bed):
		self.prefix = prefix
		self.NP = NP
		self.minK = minK
		self.maxK = maxK
		self.rep = rep
		self.cv = cv
		self.qfiles = DefaultListOrderedDict()
		self.ext = ".ped"
		if bed == True:
			self.ext = ".bed"
		self.infile = self.prefix + self.ext #build input file name based on ped/bed prefix and proper extension
		self.startdir = os.getcwd() #directory from which admixturePipeline.py was launched
		self.abspath = os.path.abspath(self.infile) #absolute path to infile
		self.outdir = os.path.dirname(self.abspath) #absolute path to directory containing infile

	def admix(self):
		ks = range(self.minK, self.maxK+1)
		#print(ks)
		#for each k value
		for i in ks:
			for j in range(self.rep):
				command_string = "admixture -j" + str(self.NP) + " -s " + str(np.random.randint(1000000)) + " --cv=" + str(self.cv) + " " + str(self.abspath) + " " + str(i)
				
				#make a temporary directory with name based on current time in milliseconds
				curtime = str(round(time.time() * 1000)) #get current time for naming directory
				newdir = os.path.join(self.outdir, curtime) #construct path to temporary directory
				os.mkdir(newdir) #make directory

				#move into temporary directory
				os.chdir(newdir)


				#call Admixture
				admixtureCall = SysCall(command_string) #prepare system call
				pathlist = os.path.split(self.prefix)
				strippedPrefix = pathlist[1] #get input file prefix - this code should still work if a relative path was used, or if the input file is in the same directory from which admixturePipeline.py was launched
				newprefix = os.path.join(self.outdir, strippedPrefix) #this 'prefix' includes the absolute path to the output directory
				admixtureCall.run_admixture(newprefix,i,j) #execute Admixture for k=i, rep=j

				#Manually re-name output files to include _j rep number
				counter = 0 #counter to track whether output files were found. Correct final number = 2
				for filename in os.listdir(newdir):
					fn = strippedPrefix + "." + str(i) + "."
					if fn in filename:
						counter+=1
						oldname, extension = os.path.splitext(filename)
						newname = oldname + "_" + str(j) + extension
						newpath = os.path.join(self.outdir, newname)
						#print(newname)
						if(extension.endswith("Q")):
							self.qfiles[str(i)].append(newname)
						os.rename(filename, newpath)
				if counter != 2:
					print("ERROR: Appropriate number of Admixture output files (N=2) was not found")
					print("This error originated from somewhere around line 64 in admixture.py")
					print("")
					raise SystemExit

				#move back to original directory
				os.chdir(self.startdir)

				#remove temporary directory
				shutil.rmtree(newdir) #need to use shutil.rmtree() because os.rmdir only deletes empty directories 

		# write dict of .Q files
		jsonFile=self.prefix + ".qfiles.json"
		with open(jsonFile, 'w') as json_file:
			json.dump(self.qfiles, json_file)

	def zipdir(self,path,ziph):
		files = [f for f in os.listdir(self.outdir) if os.path.isfile(f)]
		for root,dirs,files in os.walk(path, topdown=True):
			[dirs.remove(d) for d in list(dirs)]
			for f in files:
				if f.endswith('.Q'):
					ziph.write(os.path.join(root,f), f)

	def create_zip(self):
		resultspath = os.path.join(self.outdir, "results.zip")
		zipf = zipfile.ZipFile(resultspath, 'w', zipfile.ZIP_DEFLATED)
		self.zipdir(self.outdir, zipf)
		zipf.close()
