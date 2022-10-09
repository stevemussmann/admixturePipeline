from __future__ import print_function

import argparse
import os.path
import distutils.util

class ComLine():
	'Class for implementing command line options'


	def __init__(self, args):
		parser = argparse.ArgumentParser()
		parser._action_groups.pop()
		required = parser.add_argument_group('required arguments')
		optional = parser.add_argument_group('optional arguments')
		opt_admix = parser.add_argument_group('Admixture optional arguments')
		opt_plink = parser.add_argument_group('plink optional arguments')
		opt_vcf = parser.add_argument_group('VCFtools optional arguments')
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
		opt_admix.add_argument("-p", "--plink",
							dest='plink',
							help="Specify the prefix for a plink-formatted file. File should have been encoded in plink using the --recode12 option. This option disables ALL filtering. This is under active development. Use at your own risk."
		)
		opt_vcf.add_argument("-M", "--mac",
					dest='mac',
					type=int,
					default=0,
					help="Enter the minimum count for the minor allele filter."
		)

		opt_vcf.add_argument("-a", "--maf",
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
		opt_vcf.add_argument("-t", "--thin",
							dest='thin',
							type=int,
							default=0,
							help="Use VCFtools to thin out loci falling within the specified proximity to one another."
		)
		opt_vcf.add_argument("-r", "--remove",
							dest='remove',
							help="Specify a file of blacklisted individuals to have VCFtools remove from the analysis."
		)
		opt_vcf.add_argument("-C", "--indcov",
							dest='indcov',
							type=float,
							default=0.9,
							help="Specify the maximum allowable missing data per individual"
		)
		opt_vcf.add_argument("-S", "--snpcov",
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
		opt_vcf.add_argument("-b", "--bi",
							dest='bi',
							action='store_true',
							help="Turn off filter for biallelic SNPs."
		)

		self.args = parser.parse_args()

		#check that combinations of command line options are valid
		if all([self.args.vcf, self.args.plink]):
			print("ERROR: Cannot specify both a vcf file and a plink file as input. Use one or the other.")
			print("Exiting program...")
			print("")
			raise SystemExit
		
		if any([self.args.vcf, self.args.plink]):
			if self.args.vcf:
				print("VCF input option used.")
			if self.args.plink:
				print("Direct PLINK input option used.")
				print("Continuing with all filtering options disabled.")
		else:
			print("ERROR: Must specify either a vcf file or a plink file as input.")
			print("Exiting program...")
			print("")
			raise SystemExit
		
		#check if files exist
		print("Checking if popmap file exists.")
		self.exists( self.args.popmap )
		if self.args.vcf:
			print("Checking if .vcf file exists.")
			self.exists( self.args.vcf )
		if self.args.remove:
			print("Checking if sample removal list exists.")
			self.exists( self.args.remove )
		if self.args.plink:
			print("Checking if plink .ped file exists.")
			plinkPed = self.args.plink + ".ped"
			self.exists( plinkPed )
			print("Checking if plink .map file exists.")
			plinkMap = self.args.plink + ".map"
			self.exists( plinkMap )



	def exists(self, filename):
		if( os.path.isfile(filename) != True ):
			print(filename, "does not exist")
			print("Exiting program...")
			print("")
			raise SystemExit
		else:
			print("Found.")
			print("")
