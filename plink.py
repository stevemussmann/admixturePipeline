from __future__ import print_function

from popmap import Popmap
from syscall import SysCall

import argparse
import os.path
import shutil
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

	def filterPlink(self, keepfile, snp, maf, mac, bed, thin):
		plink_command = self.buildCommand(keepfile, snp, maf, mac, bed, thin)
		call = SysCall(plink_command)
		call.run_program()
	
	def buildCommand(self, keepfile, snp, maf, mac, bed, thin):
		command = "plink "

		# build different start to command conditional upon bed or ped input
		if bed:
			command = command + "--bfile " + self.prefix + " --make-bed "
		else:
			command = command + "--file " + self.prefix + " --recode12 "

		# filter to thin by distance between snps
		if(thin > 0):
			command = command + " --bp-space " + str(thin) + " "

		# include filter for allowable missing data per locus
		if(snp < 1.0 and snp > 0.0):
			lmiss = 1.0-snp
			command = command + "--geno " + str(lmiss) + " "
		else:
			command = command + "--geno 0.99 "

		# minor allele frequency filter
		if(maf > 0.0 and maf < 1.0):
			command = command + "--maf " + str(maf) + " "

		# minimum minor allele count filter
		if(mac > 0):
			command = command + "--mac " + str(mac) + " "

		# filter individuals
		command = command + "--keep-fam " + keepfile + " "

		# specify output
		command = command + "--out " + self.prefix

		return command

	def makeBak(self, bed):
		print("PLINK filtering will overwrite your input PLINK files.")
		print("Backups of your PLINK input files will be made if they do not already exist.")
		print("File extension .bak will be added to input files. This is done to prevent loss of data...")
		print("")
		if bed:
			b = self.prefix + ".bed"
			bim = self.prefix + ".bim"
			fam = self.prefix + ".fam"

			bb = b + ".bak"
			bimb = bim + ".bak"
			famb = fam + ".bak"

			if not os.path.isfile(bb):
				shutil.copyfile(b, bb)
			if not os.path.isfile(bimb):
				shutil.copyfile(bim, bimb)
			if not os.path.isfile(famb):
				shutil.copyfile(fam, famb)
		else:
			p = self.prefix + ".ped"
			m = self.prefix + ".map"

			pb = p + ".bak"
			mb = m + ".bak"
			
			if not os.path.isfile(pb):
				shutil.copyfile(p, pb)
			if not os.path.isfile(mb):
				shutil.copyfile(m, mb)
	
	def checkFam(self, popmap, bed):
		print("Validating sample labeling in direct input of PLINK files to ensure compatibility with pipeline...")
		d=self.parsePopmap(popmap)

		famf = str() #name of file to be parsed: .fam if bed, .ped if bed
		col1 = 0 #counts of matches to popmap dict keys in first column of famf
		col2 = 0 #counts of matches to popmap dict keys in second column of famf

		fileExt = str()
		if bed:
			fileExt = ".fam"
			famf = self.prefix + fileExt
		else:
			fileExt = ".ped"
			famf = self.prefix + ".ped"
		
		with open(famf, 'r') as f:
			for line in f:
				temp = line.split()
				if temp[0] in d:
					col1 += 1
				if temp[1] in d:
					col2 += 1

		if col1==col2 and col1==0:
			print("ERROR: Sample labels in your ", famf, " file do not match any records in ", popmap, ".")
			print("Make sure records in column 1 of", famf, "correspond to column 1 of", popmap, "before proceding.")
			print("")
			raise SystemExit
		elif col2>col1 and col1==0:
			print("ERROR:", str(col1), "records in column 1 of your", famf, "file matched any records in", popmap, ".")
			print("However,", str(col2), "records in column 2 of ", famf, "matched records in", popmap, ".")
			print("Make sure records in column 1 of", famf, "correspond to column 1 of", popmap, "before proceding.")
			print("")
			raise SystemExit
		else:
			print(str(col1), "records in column 1 of", famf, "matched records in", popmap, ".")
			print("admixturePipeline.py is assuming input PLINK files are valid. Proceeding with PLINK filtering steps.")
			print("")
			


	#adds populations to .fam file
	def fixFam(self,popmap):
		#get name for .fam file
		famf = self.prefix + ".fam"

		#read popmap into dict
		d=self.parsePopmap(popmap)

		fam=list()
		with open(famf, 'r') as f:
			for line in f:
				temp = line.split()
				temp[1] = d[temp[0]]
				newline=' '.join(temp)
				fam.append(newline)

		with open(famf, 'w') as fh:
			for line in fam:
				fh.write('%s\n' % line)
	
	def parsePopmap(self,popmap):
		d=dict()
		try:
			with open(popmap, 'r') as f:
				for line in f:
					(key, val) = line.split()
					d[key] = val
		except ValueError:
			print("Too many columns detected in your popmap file.")
			print(popmap, "may have spaces in either sample or population names.")
			print("Verify your popmap file is in the correct format and try rerunning.")
			raise SystemExit

		return d
