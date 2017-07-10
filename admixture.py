from __future__ import print_function

import argparse
import csv
import os
import os.path
import subprocess
import sys
import numpy as np
import zipfile

class Admixture():
	'Class for operating on VCF file using VCFtools and Plink'
	

	def __init__(self, prefix, NP, minK, maxK, rep):
		self.prefix = prefix
		self.NP = NP
		self.minK = minK
		self.maxK = maxK
		self.rep = rep

	def check_status(self,code, program):
		if code !=0:
			print(code)
			print("Exiting due to non-zero exit status in", program)
			raise SystemExit

	def run_program(self,string,program,i,j):
		print(string)
		try:
			fn = self.prefix + "." + str(i) + "_" + str(j) + ".stdout" #make name for stdout log file
			process = subprocess.Popen(string, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
			output, err = process.communicate()
			f = open(fn, 'w')
			f.write(output)
			f.close()
		except:
			print("Unexpected error:")
			print(sys.exc_info())
		#return_code = subprocess.check_output(string, shell=True)
		#self.check_status(return_code, program)

	def admix(self):
		ks = range(self.minK, self.maxK+1)
		print(ks)
		#for each k value
		for i in ks:
			for j in xrange(self.rep):
				command_string = "admixture -j" + str(self.NP) + " -s " + str(np.random.randint(1000000)) + " " + self.prefix + ".ped " + str(i)
				#print(command_string)
				self.run_program(command_string,"admixture",i,j)
				for filename in os.listdir("."):
					fn = self.prefix + "." + str(i) + "."
					if filename.startswith(fn):
						oldname, extension = os.path.splitext(filename)
						newname = oldname + "_" + str(j) + extension
						os.rename(filename, newname)

	def zipdir(self,path,ziph):
		files = [f for f in os.listdir('.') if os.path.isfile(f)]
		for root,dirs,files in os.walk(path):
			for f in files:
				if f.endswith('.Q'):
					ziph.write(os.path.join(root,f))

	def create_zip(self):
		zipf = zipfile.ZipFile('results.zip', 'w', zipfile.ZIP_DEFLATED)
		self.zipdir('./', zipf)
		zipf.close()

	def loglik(self):
		fh = open("loglik.txt", 'w')
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
						print(mylist)
						fh.write(kval)
						fh.write("\t")
						fh.write(mylist[-1])
						fh.write("\n")
		fh.close()
		
		try:
			command="sort -n -k1 -o loglik.txt loglik.txt"
			process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
			output, err = process.communicate()
		except:
			print("Unexpected error:")
			print(sys.exc_info())
