from evalAdmixComline import ComLine
from syscall import SysCall

from rpy2.robjects import StrVector
from rpy2.robjects.packages import STAP
from rpy2.robjects.packages import importr
from rpy2.robjects import r

import json
import os.path
import sys

class EvalAdmix():
	'Class for executing evalAdmix commands'

	def __init__(self,prefix,mc):
		self.prefix = prefix
		self.mc = mc
		self.mcOnly = False
		if(self.mc != "none"):
			self.mcOnly = True
		self.qfiles = dict()
		self.runs = dict()

		if(self.mcOnly == True):
			self.parseMC()

	def parseMC(self):
		print("Parsing MC")
		with open(self.mc) as fh:
			newlist = fh.read().splitlines()
			print(newlist)

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

				#call = SysCall(evalAdmix_str_com)
				#call.run_program()

	def averageCorres(self, funcs):
		
		#import R functions
		utils = importr('utils')
		base = importr('base')
		
		# import R plotting functions from evalAdmix
		with open(funcs, 'r') as f:
			string = f.read()
		myfunc = STAP(string, "myfunc")
		
		for k in self.runs:
			matrixList = list()
			print(k)
			for run in self.runs[k]:
				temp = run.split(".")
				temp[-1] = "corres"
				eAf = ".".join(temp)
				if(os.path.isfile(eAf)):
					cor = base.as_matrix(utils.read_table(eAf))
					matrixList.append(cor)
				else:
					print("ERROR:", eAf, "does not exist.")
					print("Exiting program...")
					raise SystemExit
			reducedList = base.Reduce('+', matrixList) #sum matrices in list
			meanList = reducedList.ro/float(len(matrixList)) #div by num elements in list to get mean


					

	def Rcode(self, funcs, minK, maxK):
	
		# import R functions
		utils = importr('utils')
		base = importr('base')
		grdevices = importr('grDevices')

		# import R plotting functions from evalAdmix
		with open(funcs, 'r') as f:
			string = f.read()
		myfunc = STAP(string, "myfunc")

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
				pop = base.as_matrix(utils.read_table(famf))
				print(qf)
				q = utils.read_table(qf)
				cor = base.as_matrix(utils.read_table(eAf))

				#print(pop)
				#print(type(pop))
				#print(pop.rx(True,2))
				#print(q)

				# run plotting functions
				ordr = myfunc.orderInds(pop=base.as_vector(pop.rx(True,2)), q=q)
				#print(type(ordr))
				#print(ordr)

				grdevices.png(file=output)
				myfunc.plotCorRes(cor_mat=cor, pop=base.as_vector(pop.rx(True,2)), ord=ordr, title=title, max_z=0.1, min_z=-0.1)
				grdevices.dev_off()
