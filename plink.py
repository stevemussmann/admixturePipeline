from __future__ import print_function

from popmap import Popmap
from syscall import SysCall

import argparse
import os.path
import subprocess
import sys

class Plink():
	'Class for executing Plink commands'

	def __init__(self,prefix):
		self.prefix = prefix

	def recodeStructure(self):
		plink_str_com = "plink --file " + self.prefix + " --allow-extra-chr 0 --recode structure --out " + self.prefix
		call = SysCall(plink_str_com)
		call.run_program()

	def recodePlink(self):
		plink_command = "plink --file " + self.prefix + " --noweb --allow-extra-chr 0 --recode12 --out " + self.prefix
		call = SysCall(plink_command)
		call.run_program()

	def makeBED(self):
		plink_command = "plink --file " + self.prefix + " --make-bed --out " + self.prefix
		call = SysCall(plink_command)
		call.run_program()

	#adds populations to .fam file
	def fixFam(self,popmap):
		#get name for .fam file
		famf = self.prefix + ".fam"

		#read popmap into dict
		d=dict()
		try:
			with open(popmap, 'r') as f:
				for line in f:
					(key, val) = line.split()
					d[key] = val
		except ValueError:
			print("Too many columns detected in your popmap file.")
			print("Your popmap file, ", popmap, ", may have spaces in either sample or population names.")
			print("Verify your popmap file is in the correct format and try rerunning.")
			raise SystemExit

		fam=list()
		with open(famf, 'r') as f:
			for line in f:
				temp = line.split()
				temp[1] = d[temp[0]]
				newline=' '.join(temp)
				fam.append(newline)

		#print(fam)

		with open(famf, 'w') as fh:
			for line in fam:
				fh.write('%s\n' % line)
