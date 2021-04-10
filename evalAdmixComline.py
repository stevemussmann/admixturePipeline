from __future__ import print_function

import argparse
import os
import distutils.util

class ComLine():
	'Class for implementing command line options'
	

	def __init__(self, args):
		parser = argparse.ArgumentParser()
		parser.add_argument("-p", "--prefix",
							dest='prefix',
							required=True,
							help="Provide the ped file prefix from your initial admixturePipeline.py run."
		)
		parser.add_argument("-k", "--minK",
							dest='minK',
							required=True,
							help="Provide the minimum K value for which you want to run evalAdmix"
		)
		parser.add_argument("-K", "--maxK",
							dest='maxK',
							required=True,
							help="Provide the maximum K value for which you want to run evalAdmix"
		)
		parser.add_argument("-m", "--popmap",
							dest='popmap',
							required=True,
							help="Provide the path to your popmap file."
		)
		parser.add_argument("-M", "--mc",
							dest='mc',
							default="MajorClusterRuns.txt",
							help="Provide path to file that will hold names of runs corresponding to the major clusters. By default it expects this file to be present in the directory from which you executed this code."
							
		)
		parser.add_argument("-R", "--evalAdmixRcode",
							dest='evalAdmixRcode',
							default="/home/mussmann/local/src/evalAdmix/visFuns.R",
							help="Provide the path to where visualization functions for evalAdmix are stored on your machine."
		)
		parser.add_argument("-n", "--np",
							dest='np',
							type=int,
							default=1,
							help="Provide the number of processors to use for evalAdmix."
		)

		self.args = parser.parse_args()

		#check if files exist
		#self.exists( self.args.cv )

		#check if directories exist
		#self.args.directory = os.path.abspath(self.args.directory)
		#self.dirExists(self.args.directory)
		if(os.path.isfile(self.args.mc) == False ):
			print( self.args.mc, "does not exist" )
			print( "Check to make sure you have specified the correct path to this file." )
			print( "Exiting program..." )
			print( "" )
			#raise SystemExit



	def exists(self, filename):
		if( os.path.isfile(filename) != True ):
			print( filename, "does not exist" )
			print( "Exiting program..." )
			print( "" )
			raise SystemExit

	def dirExists(self,directory):
		if(os.path.isdir(directory) != True):
			print(repr(directory), "does not exist")
			print("Exiting program...")
			print("")
			raise SystemExit
