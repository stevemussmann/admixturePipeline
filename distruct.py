from __future__ import print_function

from shutil import copyfile

import os
import subprocess
import sys

class Distruct():
	'Class for preparing distruct output from the output produced by clumpak'

	def __init__(self,wd,otl):
		self.wd = wd
		self.nd = os.path.join(self.wd, "best_results")

		self.oldtoplabels = otl
		self.oldbottomlabels = "bottomlabels"
		self.toplabels = os.path.join(wd,self.oldtoplabels)

		#Check if file exists
		self.fileExists(self.toplabels)

	def copyFiles(self):
		nf = os.path.join(self.nd, self.oldtoplabels)
		copyfile(self.toplabels,nf)

	def makedir(self,wd,d):
		if not os.path.exists(nd):
			os.makedirs(nd)

	def writeDrawparams(self,pfile, popq, indivq, k, outfile, pops, numind, width):
		drawp = os.path.join(self.nd, pfile)
                popqdir = os.path.join(self.nd,popq)
                indivqdir = os.path.join(self.nd,indivq)
                topdir = os.path.join(self.nd,self.oldtoplabels)
                btmdir = os.path.join(self.nd,self.oldbottomlabels)
		fh = open(drawp, 'w')
		fh.write("#define INFILE_POPQ ")
		fh.write(popqdir)
		fh.write("\n")
		fh.write("#define INFILE_INDIVQ ")
		fh.write(indivqdir)
		fh.write("\n")
		fh.write("#define INFILE_LABEL_BELOW ")
		fh.write(btmdir)
		fh.write("\n")
		fh.write("#define INFILE_LABEL_ATOP ")
		fh.write(topdir)
		fh.write("\n")
		#fh.write("#define INFILE_CLUST_PERM /home/mussmann/local/src/distruct1.1/ColorBrewer/BrBG_")
		fh.write("#define INFILE_CLUST_PERM BrBG_")
		fh.write(k)
		fh.write("_div\n")
		fh.write("#define OUTFILE ")
		fh.write(outfile)
		fh.write("\n")
		fh.write("#define K ")
		fh.write(k)
		fh.write("\n")
		fh.write("#define NUMPOPS ")
		fh.write(str(pops))
		fh.write("\n")
		fh.write("#define NUMINDS ")
		fh.write(str(numind))
		fh.write("\n")
		fh.write("#define PRINT_INDIVS 1\n")
		fh.write("#define PRINT_LABEL_ATOP 1\n")
		fh.write("#define PRINT_LABEL_BELOW 0\n")
		fh.write("#define PRINT_SEP 1\n")
		fh.write("#define FONTHEIGHT 6\n")
		fh.write("#define DIST_ABOVE -160\n")
		fh.write("#define DIST_BELOW -50\n")
		fh.write("#define BOXHEIGHT 150\n")
		fh.write("#define INDIVWIDTH ")
                fh.write(width)
                fh.write("\n")
		fh.write("#define ORIENTATION 1\n")
		fh.write("#define XORIGIN 200\n")
		fh.write("#define YORIGIN 10\n")
		fh.write("#define XSCALE 1\n")
		fh.write("#define YSCALE 1\n")
		fh.write("#define ANGLE_LABEL_ATOP 270\n")
		fh.write("#define ANGLE_LABEL_BELOW 270\n")
		fh.write("#define LINEWIDTH_RIM 3\n")
		fh.write("#define LINEWIDTH_SEP 1\n")
		fh.write("#define LINEWIDTH_IND 4\n")
		fh.write("#define GRAYSCALE 0\n")
		fh.write("#define ECHO_DATA 1\n")
		fh.write("#define REPRINT_DATA 1\n")
		fh.write("#define PRINT_INFILE_NAME 0\n")
		fh.write("#define PRINT_COLOR_BREWER 1\n")
		fh.close()

        def runDistruct(self):
                print("Now running distruct for all drawparams files...")
                contents = os.listdir(self.nd)
                
                for f in contents:
                        if f.startswith("drawparams"):
                                fpath = os.path.join(self.nd, f).rstrip()
                                print(fpath)
                                distructCommand = "distruct -d " + str(fpath)
                                self.run_program(distructCommand)

        def run_program(self, string):
                print(string)
                try:
                        process = subprocess.Popen(string, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                        output, err = process.communicate()
                        print(output)
                        print(err)
                        if process.returncode !=0:
                                    print("Non-zero exit status:")
                                    print(process.returncode)

                                    # I commented out the raise SystemExit here because distruct always seems to exit with a non-zero status.
                                    #raise SystemExit
                except (KeyboardInterrupt, SystemExit):
                        raise
                except:
                        print("Unexpected error:")
                        print(sys.exc_info())
                        raise SystemExit


	def fileExists(self, filename):
		if( os.path.isfile(filename) != True ):
			print( filename, "does not exist" )
			print( "Exiting program..." )
			print( "" )
			raise SystemExit
		else:
			print(filename, "Exists")
