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
		parser.add_argument("-p", "--prefix",
							dest='prefix',
							required=True,
							help="Specify the prefix from your admixpipe run. This will be the same name as your VCF file without the .vcf file extension."
		)
		parser.add_argument("-e", "--email",
							dest='email',
							required=True,
							help="Specify your email address for the CLUMPAK submission form."
		)
		
		self.args = parser.parse_args()

		#check if files exist
		self.exists( self.args.results )

	def exists(self, filename):
		if( os.path.isfile(filename) != True ):
			print( filename, "does not exist" )
			print( "Exiting program..." )
			print( "" );
			raise SystemExit
