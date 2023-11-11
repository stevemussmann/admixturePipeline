from __future__ import print_function

import argparse
import os.path
import distutils.util

class ComLine():
	'Class for implementing command line options'


	def __init__(self, args):
		parser = argparse.ArgumentParser()
		parser._action_groups.pop()
		required = parser.add_argument_group('Required arguments (only one of -v, -b, or -p is required)')
		optional = parser.add_argument_group('Optional arguments')
		opt_admix = parser.add_argument_group('Admixture optional arguments')
		opt_filt = parser.add_argument_group('Filtering arguments (compatible with VCFtools and PLINK)')
		opt_vcf = parser.add_argument_group('VCFtools filtering arguments')
		required.add_argument("-m", "--popmap",
							dest='popmap',
							required=True,
							help="Specify a tab-delimited population map (sample -> population)"
		)
		required.add_argument("-v", "--vcf",
							dest='vcf',
							help="Specify a vcf file for input."
		)
		opt_admix.add_argument("-k", "--minK",
							dest='minK',
							type=int,
							default=1,
							help="minimum K value."
		)
		opt_admix.add_argument("-K", "--maxK",
							dest='maxK',
							type=int,
							default=20,
							help="maximum K value."
		)
		required.add_argument("-p", "--ped",
							dest='ped',
							help="Specify the prefix for a text plink file. File should have been encoded in plink using the --recode12 option. This is under active development. Use at your own risk."
		)
		required.add_argument("-b", "--bed",
							dest='bed',
							help="Specify the prefix for a binary plink file. This is under active development. Use at your own risk."
		)
		opt_filt.add_argument("-M", "--mac",
							dest='mac',
							type=int,
							default=0,
							help="Enter the minimum count for the minor allele filter."
		)
		opt_filt.add_argument("-a", "--maf",
							dest='maf',
							type=float,
							default=0.0,
							help="Enter the minimum frequency for the minor allele filter."
		)
		optional.add_argument("-n", "--np",
							dest='np',
							type=int,
							default=1,
							help="Number of processors."
		)
		opt_filt.add_argument("-t", "--thin",
							dest='thin',
							type=int,
							default=0,
							help="Use VCFtools or PLINK to thin out loci falling within the specified proximity to one another."
		)
		opt_vcf.add_argument("-C", "--indcov",
							dest='indcov',
							type=float,
							default=0.9,
							help="Specify the maximum allowable missing data per individual"
		)
		opt_filt.add_argument("-S", "--snpcov",
							dest='snpcov',
							type=float,
							default=0.1,
							help="Specify the allowable proportion of missing data per SNP. 0 allows sites that are completely missing and 1 indicates no missing data allowed."
		)
		opt_admix.add_argument("-c", "--cv",
							dest='cv',
							type=int,
							default=20,
							help="Specify the cross-validation number for admixture program"
		)
		opt_admix.add_argument("-R", "--rep",
							dest='rep',
							type=int,
							default=20,
							help="Number of replicates per K."
		)
		opt_vcf.add_argument("-B", "--bi",
							dest='bi',
							action='store_true',
							help="Turn off filter for biallelic SNPs."
		)

		self.args = parser.parse_args()

		#check that combinations of command line options are valid
		booleans=[self.args.vcf, self.args.ped, self.args.bed]
		if self.xOrMoreAreTrue(booleans) > 1:
			print("ERROR: Only one of a bed, ped, or vcf file can be used as input.")
			print("Exiting program...")
			print("")
			raise SystemExit
		elif any([self.args.vcf, self.args.ped, self.args.bed]):
			if self.args.vcf:
				print("VCF input option used.")
			if self.args.ped:
				print("PLINK ped input option used.")
				print("Continuing with all filtering options disabled.")
			if self.args.bed:
				print("PLINK bed input option used.")
				print("Continuing with all filtering options disabled.")
		else:
			print("ERROR: Must specify either a VCF file or a PLINK file (bed or ped) as input.")
			print("Exiting program...")
			print("")
			raise SystemExit
		
		#check if files exist
		print("Checking if popmap file exists...")
		self.exists( self.args.popmap )
		if self.args.vcf:
			print("Checking if VCF file exists...")
			self.exists( self.args.vcf )
		if self.args.ped:
			print("Checking if plink .ped file exists...")
			plinkPed = self.args.ped + ".ped"
			self.exists( plinkPed )
			print("Checking if plink .map file exists...")
			plinkMap = self.args.ped + ".map"
			self.exists( plinkMap )
		if self.args.bed:
			print("Checking if plink .bed file exists...")
			plinkBed = self.args.bed + ".bed"
			self.exists( plinkBed )
			print("Checking if plink .bim file exists...")
			plinkBim = self.args.bed + ".bim"
			self.exists( plinkBim )
			print("Checking if plink .fam file exists...")
			plinkFam = self.args.bed + ".fam"
			self.exists( plinkFam )

	def exists(self, filename):
		if( os.path.isfile(filename) != True ):
			print(filename, "does not exist")
			print("Exiting program...")
			print("")
			raise SystemExit
		else:
			print("Found.")
			print("")
	
	def xOrMoreAreTrue(self, booleans):
		count = 0
		for boolean in booleans:
			if(boolean):
				count += 1
		return count
