from __future__ import print_function

import argparse
import os.path

class ComLine():
	'Class for implementing command line options'
	

	def __init__(self, args):
		parser = argparse.ArgumentParser()
		parser.add_argument("-c", "--cv",
							dest='cv',
							default="cv_file.txt",
							help="Provide a file with cross-validation values for multiple admixture runs"
		)
		parser.add_argument("-o", "--out",
							dest='out',
							default="output.txt",
							help="Specify an output file name."
		)
		
		self.args = parser.parse_args()

		#check if files exist
		self.exists( self.args.cv )



	def exists(self, filename):
		if( os.path.isfile(filename) != True ):
			print( filename, "does not exist" )
			print( "Exiting program..." )
			print( "" );
			raise SystemExit
