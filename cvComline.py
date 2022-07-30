from __future__ import print_function

import argparse
import os.path

class ComLine():
	'Class for implementing command line options'
	
	def __init__(self, args):
		parser = argparse.ArgumentParser()
		parser.add_argument("-c", "--cv",
							dest='cv',
							default="cv_file.MajClust.txt",
							help="Provide a file with cross-validation values for multiple admixture runs"
		)
		parser.add_argument("-l", "--loglik",
							dest='ll',
							default="loglikelihood_file.MajClust.txt",
							help="Provide a file with loglikelihood values for multiple admixture runs"
		)
		parser.add_argument("-o", "--cvout",
							dest='out',
							default="cv_output.txt",
							help="Specify an output file name for cv values."
		)
		parser.add_argument("-L", "--llout",
							dest='llout',
							default="ll_output.txt",
							help="Specify an output file name for loglikelihood values."
		)
		
		self.args = parser.parse_args()

		#check if files exist
		self.exists( self.args.cv )
		self.exists( self.args.ll )

	def exists(self, filename):
		if( os.path.isfile(filename) != True ):
			print( filename, "does not exist" )
			print( "Have you run distructRerun.py yet?" )
			print( "Exiting program..." )
			print( "" );
			raise SystemExit
