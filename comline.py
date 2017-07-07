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
							default="input.vcf",
							help="Specify a phylip file for input."
		)
		parser.add_argument("-o", "--out",
							dest='out',
							default="output.txt",
							help="Specify an output file name."
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
