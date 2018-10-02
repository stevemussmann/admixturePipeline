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


	def __init__(self, prefix, NP, minK, maxK, rep, cv):
		self.prefix = prefix
		self.NP = NP
		self.minK = minK
		self.maxK = maxK
		self.rep = rep
		self.cv = cv

	def run_program(self,string,i,j):
		print(string)
		try:
			fn = self.prefix + "." + str(i) + "_" + str(j) + ".stdout" #make name for stdout log file
			process = subprocess.Popen(string, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
			output, err = process.communicate()
			f = open(fn, 'w')
			f.write(output)
			f.close()
			print(err)
			if process.returncode !=0:
				print("Non-zero exit status:")
				print(process.returncode)
				raise SystemExit
		except (KeyboardInterrupt, SystemExit):
			raise
		except:
			print("Unexpected error:")
			print(sys.exc_info())
			raise SystemExit

	def admix(self):
		ks = range(self.minK, self.maxK+1)
		print(ks)
		#for each k value
		for i in ks:
			for j in xrange(self.rep):
				command_string = "admixture -j" + str(self.NP) + " -s " + str(np.random.randint(1000000)) + " --cv=" + str(self.cv) + " " + self.prefix + ".ped " + str(i)
				#print(command_string)
				self.run_program(command_string,i,j)

				#Manually re-name output files to include _j rep number
				# oldP = self.prefix + "." + str(i) + ".P"
				# newP = self.prefix + "." + str(i) + "_" + str(j) + ".P"
				# os.rename(oldP, newP)
				# oldQ = self.prefix + "." + str(i) + ".Q"
				# newQ = self.prefix + "." + str(i) + "_" + str(j) + ".Q"
				# os.rename(oldQ, newQ)
				for filename in os.listdir("."):
					fn = self.prefix + "." + str(i) + "."
					if fn in filename:
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

	def print_cv(self):
		try:
			command="grep -h CV " + self.prefix + "*.stdout > " + self.prefix + "_cv_summary.txt"
			process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
			output,err = process.communicate()
			print(err)
			if process.returncode != 0:
				print("Non-zero exit status:")
				print(process.returncode)
				raise SystemExit
		except:
			print("Unexpected error:")
			print(sys.exc_info())
			raise SystemExit

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
						#print(mylist)
						fh.write(kval)
						fh.write("\t")
						fh.write(mylist[-1])
						fh.write("\n")
				temp.close()
		fh.close()

		try:
			command="sort -n -k1 -o loglik.txt loglik.txt"
			process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
			output, err = process.communicate()
			print(err)
			if process.returncode != 0:
				print("Non-zero exit status:")
				print(process.returncode)
				raise SystemExit
		except:
			print("Unexpected error:")
			print(sys.exc_info())
			raise SystemExit
