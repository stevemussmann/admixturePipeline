from __future__ import print_function

from popmap import Popmap

import argparse
import os.path
import subprocess
import sys

class VCF():
	'Class for operating on VCF file using VCFtools and Plink'
	
	def __init__(self, infile, thin, maf):
		self.vcf_file = infile
		self.thin = thin
		self.maf = maf

		temp = os.path.splitext(os.path.basename(infile))
		self.prefix = temp[0]

	def run_program(self,string):
		print(string)
		try:
			process = subprocess.Popen(string, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
			output, err = process.communicate()
			print(err)
			if process.returncode != 0:
				print("Non-zero exit status:")
				print(process.returncode)
				raise SystemExit
		except:
			print("Unexpected error:")
			print(sys.exec_info())
			raise SystemExit

	def fix_map(self):
		name = self.prefix + ".map"
		data = self.readfile(name)

		f = open(name,'w')
		for line in data:
			newline = "l" + line.rstrip()
			f.write(newline)
			f.write('\n')
		f.close()

	def convert(self):
		vcf_command = "vcftools --vcf " + self.vcf_file + " --plink --out " + self.prefix
		if(self.thin > 0):
			vcf_command = vcf_command + " --thin " + str(self.thin)
		self.run_program(vcf_command)

		self.fix_map()

	def plink(self):
		plink_command = "plink --file " + self.prefix + " --noweb --allow-extra-chr 0 --recode12 --out " + self.prefix
		if(self.maf > 0):
			maf_float = self.maf/100.0
			plink_command = plink_command + " --maf " + str(maf_float)
		self.run_program(plink_command)

	def print_populations(self,popmap):
		data = self.readfile(self.vcf_file)
		popfile = self.prefix + "_pops.txt"
		f = open(popfile,'w')
		for line in data:
			if line.startswith("#CHROM"):
				mylist = line.split()
				del mylist[0:9]
				print(mylist)
				for ind in mylist:
					ind.strip('\t\n\r')
					#print(popmap.get_pop(ind))
					f.write(popmap.get_pop(ind))
					f.write("\n")
		f.close()

	def readfile(self,infile):
		f=open(infile)
		data = f.readlines()
		f.close()
		return data
