from __future__ import print_function

from syscall import SysCall

import argparse
import csv
import os
import os.path
import subprocess
import sys
import numpy as np
import zipfile

class Admixture():
	'Class for executing Admixture commands'


	def __init__(self, prefix, NP, minK, maxK, rep, cv):
		self.prefix = prefix
		self.NP = NP
		self.minK = minK
		self.maxK = maxK
		self.rep = rep
		self.cv = cv

	def admix(self):
		ks = range(self.minK, self.maxK+1)
		#print(ks)
		#for each k value
		for i in ks:
			for j in range(self.rep):
				command_string = "admixture -j" + str(self.NP) + " -s " + str(np.random.randint(1000000)) + " --cv=" + str(self.cv) + " " + self.prefix + ".ped " + str(i)
				
				#call Admixture
				admixtureCall = SysCall(command_string)
				admixtureCall.run_admixture(self.prefix,i,j)

				#Manually re-name output files to include _j rep number
				for filename in os.listdir("."):
					fn = self.prefix + "." + str(i) + "."
					if fn in filename:
						oldname, extension = os.path.splitext(filename)
						newname = oldname + "_" + str(j) + extension
						os.rename(filename, newname)

	def zipdir(self,path,ziph):
		files = [f for f in os.listdir('.') if os.path.isfile(f)]
		for root,dirs,files in os.walk(path, topdown=True):
			[dirs.remove(d) for d in list(dirs)]
			for f in files:
				if f.endswith('.Q'):
					ziph.write(os.path.join(root,f))

	def create_zip(self):
		zipf = zipfile.ZipFile('results.zip', 'w', zipfile.ZIP_DEFLATED)
		self.zipdir('./', zipf)
		zipf.close()

	def print_cv(self):
		print("Printing CV values...")
		command="grep -h CV " + self.prefix + "*.stdout > " + self.prefix + "_cv_summary.txt"

		grepCall = SysCall(command)
		grepCall.run_program()

	def loglik(self):
		fh = open("loglik.txt", 'wb')
		for fn in os.listdir("."):
			if fn.endswith("stdout"):
				temp = open(fn, 'r')
				fnlist = fn.split("_")
				fnlist2 = fnlist[-2].split(".")
				kval = fnlist2[-1]
				print(fnlist2)
				for line in temp.readlines():
					if line.startswith("Loglikelihood:"):
						mylist = line.split()
						#print(mylist)
						fh.write(kval.encode())
						fh.write("\t".encode())
						fh.write(mylist[-1].encode())
						fh.write("\n".encode())
				temp.close()
		fh.close()

		print("Sorting log(likelihood) values...")
		command="sort -n -k1 -o loglik.txt loglik.txt"

		sortCall = SysCall(command)
		sortCall.run_program()
