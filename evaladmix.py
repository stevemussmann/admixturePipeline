from evalAdmixComline import ComLine
from syscall import SysCall

from rpy2.robjects import StrVector
from rpy2.robjects.conversion import localconverter
from rpy2.robjects.packages import STAP
from rpy2.robjects.packages import importr
from rpy2.robjects import r, pandas2ri

import json
import os.path
import pandas
import rpy2.robjects
import sys

class EvalAdmix():
	'Class for executing evalAdmix commands'

	def __init__(self,prefix,mc,funcs):
		self.prefix = prefix
		self.mc = mc
		self.mcOnly = False
		if(self.mc != "none"):
			self.mcOnly = True
		self.qfiles = dict()
		self.runs = dict()
		self.qfilePaths = dict()

		if(self.mcOnly == True):
			self.parseMC()
		
		#import R functions
		self.utils = importr('utils')
		self.base = importr('base')
		self.grdevices = importr('grDevices')
		
		# import R plotting functions from evalAdmix
		with open(funcs, 'r') as f:
			string = f.read()
		self.myfunc = STAP(string, "myfunc")
		

	def parseMC(self):
		print("Parsing MC")
		with open(self.mc) as fh:
			newlist = fh.read().splitlines()
			print(newlist)

	def loadJson(self):
		self.loadQ()
		self.loadRuns()
		self.loadQfilePaths()

	def loadQ(self):
		qfn = self.prefix + ".qfiles.json"
		if os.path.isfile(qfn):
			with open(qfn) as fh:
				self.qfiles = json.load(fh)
		else:
			print("ERROR:", qfn, "does not exist.")
			print("Exiting program...")
			raise SystemExit
	
	def loadRuns(self):
		rfn = "cvRuns.json"
		if os.path.isfile(rfn):
			with open(rfn) as fh:
				self.runs = json.load(fh)
		else:
			print("ERROR:", rfn, "does not exist.")
			print("Exiting program...")
			raise SystemExit

	def loadQfilePaths(self):
		rfn = "qfilePaths.json"
		if os.path.isfile(rfn):
			with open(rfn) as fh:
				self.qfilePaths = json.load(fh)
		else:
			print("ERROR:", rfn, "does not exist.")
			print("Exiting program...")
			raise SystemExit

	def evalAdmix(self, minK, maxK, np):
		ks = range(int(minK), int(maxK)+1)
		for k in ks:
			for qf in self.qfiles[str(k)]:
				print(qf)
				temp = qf.split(".")

				#make .P file name
				temp[-1] = "P"
				pf = ".".join(temp)

				#make output .corres file name
				temp[-1] = "corres"
				eAf = ".".join(temp)

				#build command for evalAdmix
				evalAdmix_str_com = "evalAdmix -plink " + self.prefix + " -fname " + pf + " -qname " + qf + " -o " + eAf + " -P " + str(np)

				call = SysCall(evalAdmix_str_com)
				call.run_program()

	def averageCorres(self, funcs):
		
		for k in self.runs:
			matrixList = list()
			print(k)
			for run in self.runs[k]:
				temp = run.split(".")
				temp[-1] = "corres"
				eAf = ".".join(temp)
				if(os.path.isfile(eAf)):
					cor = self.base.as_matrix(self.utils.read_table(eAf))
					matrixList.append(cor)
				else:
					print("ERROR:", eAf, "does not exist.")
					print("Exiting program...")
					raise SystemExit
			reducedList = self.base.Reduce('+', matrixList) #sum matrices in list
			cor = reducedList.ro/float(len(matrixList)) #div by num elements in list to get mean
			q = self.parseClumpp(self.qfilePaths[k])
			#check if object q is NoneType
			if q is None:
			    print("Empty matrices (Python NoneType) were returned When trying to create average matrices for Major/Minor clusters.")
			    print("Check that the paths in qfilePaths.json are valid.")
			    print("This error could occur if you have moved your admixture run folder after running distructRerun.py.")
			    print("Alternatively, if you are using the Docker container this could have occurred if you ran distructRerun.py on your own system outside of the container.")
			    raise SystemExit

			famf = self.prefix + ".fam"
			pop = self.base.as_matrix(self.utils.read_table(famf))

			# uncomment below lines for debugging.
			#print(type(pop))
			#print(type(famf))

			output = k + ".png"
			ordr = self.myfunc.orderInds(pop=self.base.as_vector(pop.rx(True,2)), q=q)
			title=k

			self.grdevices.png(file=output)
			try:
				self.myfunc.plotCorRes(cor_mat=cor, pop=self.base.as_vector(pop.rx(True,2)), ord=ordr, title=title, max_z=0.1, min_z=-0.1)
			except rpy2.rinterface_lib.embedded.RRuntimeError:
				print("Error in R code (plotting functions) from evalAdmix.")
			self.grdevices.dev_off()

	def parseClumpp(self,f):
		if(os.path.isfile(f)):
			df = pandas.read_csv(f, delimiter="\s+", header=None, index_col=False)

			# Even though inplace=True is used in this contect, operating on the dataframe directly rather than assigning to a new variable should prevent creation of a "NoneType"
			df.drop(df.columns[0:5],axis=1,inplace=True)
		
			# uncomment below lines for debugging.
			#print(type(df))
			#print(df)

			with localconverter(rpy2.robjects.default_converter + pandas2ri.converter):
				Rdf = rpy2.robjects.conversion.py2rpy(df)

			#print(type(Rdf))
			#print(Rdf)
			return Rdf

	def Rcode(self, funcs, minK, maxK):
		#make file names
		famf = self.prefix + ".fam"

		ks = range(int(minK), int(maxK)+1)
		for k in ks:
			title="K="+str(k)
			for qf in self.qfiles[str(k)]:
				temp = qf.split(".")
				temp[-1] = "corres"
				eAf = ".".join(temp)
				output = eAf + ".png"

				# read in files
				pop = self.base.as_matrix(self.utils.read_table(famf))
				print(qf)
				q = self.utils.read_table(qf)
				cor = self.base.as_matrix(self.utils.read_table(eAf))

				print(type(pop))
				print(type(famf))

				# run plotting functions
				ordr = self.myfunc.orderInds(pop=self.base.as_vector(pop.rx(True,2)), q=q)

				self.grdevices.png(file=output)
				try:
					self.myfunc.plotCorRes(cor_mat=cor, pop=self.base.as_vector(pop.rx(True,2)), ord=ordr, title=title, max_z=0.1, min_z=-0.1)
				except rpy2.rinterface_lib.embedded.RRuntimeError:
					print("Something happened.")
				self.grdevices.dev_off()
