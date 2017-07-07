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

	def convert():
		command_string = "vcftools --vcf " + self.infile + " --plink --out " + self.prefix
		print(command_string)
		#return_code = subprocess.call()
