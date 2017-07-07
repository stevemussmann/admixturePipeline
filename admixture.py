from __future__ import print_function

import argparse
import os
import os.path
import subprocess
import numpy as np

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

	def run_program(self,string,program):
		print(string)
		return_code = subprocess.call(string, shell=True)
		self.check_status(return_code, program)

	def admix(self):
		ks = range(self.minK, self.maxK+1)
		print(ks)
		#for each k value
		for i in ks:
			for j in xrange(self.rep):
				command_string = "admixture -j" + str(self.NP) + " -s " + str(np.random.randint(1000000)) + " " + self.prefix + ".ped " + str(i)
				print(command_string)
				self.run_program(command_string,"admixture")
				for filename in os.listdir("."):
					fn = self.prefix + "." + str(i) + "."
					if filename.startswith(fn):
						oldname, extension = os.path.splitext(filename)
						newname = oldname + "_" + str(j) + extension
						os.rename(filename, newname)
