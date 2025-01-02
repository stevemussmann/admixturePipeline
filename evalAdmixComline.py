from __future__ import print_function

import argparse
import os
import distutils.util

class ComLine():
	'Class for implementing command line options'
	

	def __init__(self, args):
		parser = argparse.ArgumentParser()
		parser.add_argument("-b", "--bed",
							dest='bed',
							action='store_true',
							help="Boolean switch to convert .ped to .bed format (default = false). Use this option if you used the -b/--bed option when running admixturePipeline.py"
		)
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
							default="none",
							help="Provide path to file that will hold names of runs corresponding to the major clusters."
							
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
		if(self.args.mc != "none"):
			self.exists(self.args.mc)
		if(self.args.bed):
			print("Checking for plink text format files. If these checks fail, you may need to use the -b/--bed option.")
			print("Checking if plink .ped file exists...")
			plinkPed = self.args.prefix + ".ped"
			self.exists( plinkPed )
			print("Checking if plink .map file exists...")
			plinkMap = self.args.prefix + ".map"
			self.exists( plinkMap )
		else:
			print("Checking for plink binary format files. If these checks fail, you may need to drop the -b/--bed option.")
			print("Checking if plink .bed file exists...")
			plinkBed = self.args.prefix + ".bed"
			self.exists( plinkBed )
			print("Checking if plink .bim file exists...")
			plinkBim = self.args.prefix + ".bim"
			self.exists( plinkBim )
			print("Checking if plink .fam file exists...")
			plinkFam = self.args.prefix + ".fam"
			self.exists( plinkFam )



	def exists(self, filename):
		if( os.path.isfile(filename) != True ):
			print( filename, "does not exist." )
			print( "Check to make sure you have specified the correct path to this file." )
			print( "Exiting program..." )
			print( "" )
			raise SystemExit
		else:
			print("Found.")
			print("")

	def dirExists(self,directory):
		if(os.path.isdir(directory) != True):
			print(repr(directory), "does not exist")
			print("Exiting program...")
			print("")
			raise SystemExit
