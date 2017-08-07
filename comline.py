from __future__ import print_function

import argparse
import os.path

class ComLine():
	'Class for implementing command line options'
	

	def __init__(self, args):
		parser = argparse.ArgumentParser()
		parser.add_argument("-m", "--popmap",
							dest='popmap',
							default="map.txt",
							help="Specify a tab-delimited population map (sample -> population)"
		)
		parser.add_argument("-v", "--vcf",
							dest='vcf',
							required=True,
							help="Specify a phylip file for input."
		)
		parser.add_argument("-o", "--out",
							dest='out',
							default="output.txt",
							help="Specify an output file name."
		)
		#parser.add_argument("-f", "--filter",
		#					dest='filter',
		#					default=False,
		#					action='store_true',
		#					help="Turn on filtering in plink."
		#)
		parser.add_argument("-k", "--minK",
							dest='minK',
							type=int,
							default=1,
							help="minimum K value."
		)
		parser.add_argument("-K", "--maxK",
							dest='maxK',
							type=int,
							default=20,
							help="maximum K value."
		)
		parser.add_argument("-n", "--np",
							dest='np',
							type=int,
							default=1,
							help="Number of processors."
		)
		parser.add_argument("-t", "--thin",
							dest='thin',
							type=int,
							default=0,
							help="Use VCFtools to thin out loci falling within the specified proximity to one another. -f must also be used to turn on filtering"
		)
		parser.add_argument("-c", "--cv",
							dest='cv',
							type=int,
							default=20,
							help="Specify the cross-validation number for admixture program"
		)
		parser.add_argument("-R", "--rep",
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
