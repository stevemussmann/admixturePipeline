from __future__ import print_function

from popmap import Popmap
from plink import Plink
from syscall import SysCall

import argparse
import os.path
import subprocess
import sys

class VCF():
	'Class for operating on VCF file using VCFtools and Plink'

	def __init__(self, infile, thin, maf, mac, ind, snp, bi, r):
		self.vcf_file = infile
		self.thin = thin
		self.maf = maf
		self.mac = mac
		self.ind = ind #maximum allowable missing data per snp
		self.snp = snp #maximum allowable missing data per individual
		self.bi = bi #controls biallelic filter
		self.removeFile = r #file containing individuals to be removed
		self.removeInds = False
		self.blacklist = dict() #make dictionary of blacklisted individuals
		if self.removeFile:
			self.removeInds = True

		temp = os.path.splitext(os.path.basename(infile))
		self.prefix = temp[0]
		self.get_indlist()

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

		if(self.ind < 1.0 and self.ind > 0.0):
			remove = self.get_ind_coverage()
			#print(remove)

		vcf_command = "vcftools --vcf " + self.vcf_file + " --plink --out " + self.prefix
		if(self.thin > 0):
			vcf_command = vcf_command + " --thin " + str(self.thin)
		if(self.snp < 1.0 and self.snp > 0.0):
			vcf_command = vcf_command + " --max-missing " + str(self.snp)
		if(len(remove) > 0):
			vcf_command = vcf_command + remove
		if(self.maf > 0.0 and self.maf < 1.0):
			vcf_command = vcf_command + " --maf " + str(self.maf)
		if(self.mac > 0):
			vcf_command = vcf_command + " --mac " + str(self.mac)
		if(self.bi == True):
			vcf_command = vcf_command + " --min-alleles 2 --max-alleles 2"
		if(self.removeInds == True ):
			vcf_command = vcf_command + " --remove " + str(self.removeFile)

		call = SysCall(vcf_command)
		call.run_program()

		self.fix_map()

	def get_ind_coverage(self):
		vcf_command = "vcftools --vcf " + self.vcf_file + " --missing-indv --out " + self.prefix
		if( self.removeInds == True ):
			vcf_command = vcf_command + " --remove " + str(self.removeFile)

		call = SysCall(vcf_command)
		call.run_program()

		fname = self.prefix + ".imiss"
		ret = ""
		with open(fname, 'r') as fh:
			try:
				lnum = 0
				for line in fh:
					line = line.strip()
					if not line:
						continue
					lnum+=1
					if lnum <2: #skip header line
						continue
					else:
						stuff = line.split()
						#print(stuff)
						if float(stuff[4]) > self.ind:
							print("Removing individual %s: %s missing data"%(stuff[0],stuff[4]))
							self.blacklist[stuff[0]]=1
							ret = ret + " --remove-indv " + str(stuff[0])
				return(ret)
			except IOError as e:
				print("Could not read file %s: %s"%(fname,e))
				sys.exit(1)
			except Exception as e:
				print("Unexpected error reading file %s: %s"%(fname,e))
				sys.exit(1)
			finally:
				fh.close()

	def plink(self):
		pl = Plink(self.prefix)
		pl.recodeStructure()
		pl.recodePlink()

	def get_indlist(self):
		string_vtools = "vcf-query -l " + self.vcf_file + " > vcf_indlist.txt"
		string_btools = "bcftools query -l " + self.vcf_file + " > vcf_indlist.txt"

		try: 
			print(string_btools)
			self.runCode(string_btools)
		except:
			try:
				print("BCFtools failed.")
				print(string_vtools)
				self.runCode(string_vtools)
			except:
				print("VCFtools failed.")


	def print_populations(self,popmap):
		if(self.removeInds == True):
			rmf = self.readfile(self.removeFile)
			for key in rmf:
				key.rstrip()
				self.blacklist[key]=1 

		#print(self.blacklist)

		#print populations file, excluding blacklisted individuals
		data = self.readfile(self.vcf_file)
		popfile = self.prefix + "_pops.txt"
		f = open(popfile,'w')
		for ind in popmap.get_list():
			if ind not in self.blacklist:
				f.write(popmap.get_pop(ind))
				f.write("\n")
		f.close()

	def print_individuals(self,popmap):
		if(self.removeInds == True):
			rmf = self.readfile(self.removeFile)
			for key in rmf:
				key.rstrip()
				self.blacklist[key]=1 

		#print(self.blacklist)

		#print populations file, excluding blacklisted individuals
		data = self.readfile(self.vcf_file)
		popfile = self.prefix + "_inds.txt"
		f = open(popfile,'w')
		for ind in popmap.get_list():
			if ind not in self.blacklist:
				f.write(ind)
				f.write("\n")
		f.close()


	def readfile(self,infile):
		f=open(infile)
		data = f.read().splitlines()
		f.close()
		return data
