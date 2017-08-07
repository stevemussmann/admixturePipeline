from __future__ import print_function

import argparse
import os.path

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
							required=True,
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
		opt_plink.add_argument("-a", "--maf",
							dest='maf',
							type=int,
							default=0,
							help="Enter the minimum frequency for the minor allele frequency filter as an integer.  For example, 1 = 0.01"
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
		
		self.args = parser.parse_args()

		#check if files exist
		self.exists( self.args.popmap )
		self.exists( self.args.vcf )



	def exists(self, filename):
		if( os.path.isfile(filename) != True ):
			print(filename, "does not exist")
			print("Exiting program...")
			print("")
			raise SystemExit
