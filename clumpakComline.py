import argparse
import os.path

class ComLine():
	'Class for implementing command line options'

	def __init__(self, args):
		parser = argparse.ArgumentParser()
		parser.add_argument("-r", "--results",
							dest='results',
							default="results.zip",
							help="Provide the results.zip file from your admixpipe run. Specifying the name is only necessary if you have changed it from the default results.zip."
		)
		parser.add_argument("-l", "--ll",
							dest='ll',
							default="ll_all.txt",
							help="Provide the tab delmimited file of log likelihood values. Specifying the name is only necessary if you have changed it from the default ll_all.txt from the distructRerun.py module.."
		)
		parser.add_argument("-p", "--prefix",
							dest='prefix',
							help="Specify the prefix from your admixpipe run. This will be the same name as your VCF file without the .vcf file extension. Required for -w and -M options."
		)
		parser.add_argument("-e", "--email",
							dest='email',
							help="Specify your email address for the CLUMPAK submission form. Required for -w option."
		)
		parser.add_argument("-m", "--MCL",
							dest='MCL',
							#default=1.0,
							type=float,
							help="[optional] Provide user-defined MCL threshold for similarity scores. Must be >=0 and <=0.99."
		)
		parser.add_argument("-d", "--DISTRUCT",
							dest='DISTRUCT',
							#default=1.0,
							type=float,
							help="[optional] Provide user-defined DISTRUCT threshold for minimal. Must be >=0 and <=0.95."
		)
		parser.add_argument("-w", "--web",
							dest='web',
							action='store_true',
							help="Submit to CLUMPAK server instead of running locally."
		)
		parser.add_argument("-x", "--overwrite",
							dest='overwrite',
							action='store_true',
							help="Overwrite existing CLUMPAK output directory."
		)
		parser.add_argument("-M", "--mainpipeline",
							dest='mainpipeline',
							action='store_true',
							help="Run CLUMPAK main pipeline locally."
		)
		parser.add_argument("-b", "--bestk",
							dest='bestk',
							action='store_true',
							help="Run CLUMPAK BestK pipeline locally."
		)
		
		self.args = parser.parse_args()

		booleans=[self.args.web, self.args.mainpipeline, self.args.bestk]
		if self.xOrMoreAreTrue(booleans) > 1:
			print("Only one CLUMPAK pipeline option can be used at once (-b, -M, or -w).")
			print("Exiting program...")
			print("")
			raise SystemExit
		elif any(booleans):
			if self.args.web:
				print("Attempting to submit to CLUMPAK web server.")
				#check if files exist
				self.exists( self.args.results )
				if not self.args.email:
					print("Must specify email address with -e option.")
					print("")
					raise SystemExit
				if not self.args.prefix:
					print("Must specify prefix of your input .vcf or PLINK files with -p option.")
					print("")
					raise SystemExit
			if self.args.mainpipeline:
				print("Running CLUMPAK main pipeline locally.")
				#check if files exist
				self.exists( self.args.results )
				if not self.args.prefix:
					print("Must specify prefix of your input .vcf or PLINK files with -p option.")
					print("")
					raise SystemExit
			if self.args.bestk:
				print("Running CLUMPAK bestk pipeline locally.")
				#check if files exist
				self.exists( self.args.ll )
		else:
			print("ERROR: Must specify one of the CLUMPAK pipeline options (-b, -M, or -w).")
			print("Exiting program...")
			print("")
			raise SystemExit


	def exists(self, filename):
		if( os.path.isfile(filename) != True ):
			print( filename, "does not exist" )
			print( "Exiting program..." )
			print( "" );
			raise SystemExit
	
	def xOrMoreAreTrue(self, booleans):
		count = 0
		for boolean in booleans:
			if(boolean):
				count += 1
		return count
