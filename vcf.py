from __future__ import print_function

import argparse
import os.path
import subprocess

class VCF():
	'Class for operating on VCF file using VCFtools and Plink'
	

	def __init__(self, infile):
		self.vcf_file = infile
		temp = os.path.splitext(infile)
		self.prefix = temp[0]

	def check_status(self,code, program):
		if code !=0:
			print(code)
			print("Exiting due to non-zero exit status in", program)
			raise SystemExit

	def run_program(self,string,program):
		print(string)
		return_code = subprocess.call(string, shell=True)
		self.check_status(return_code, program)

	def convert(self):
		vcf_command = "vcftools --vcf " + self.vcf_file + " --plink --out " + self.prefix
		plink_command = "plink --file " + self.prefix + " --noweb --recode12 --out " + self.prefix

		self.run_program(vcf_command, "VCFtools")
		self.run_program(plink_command, "plink")
