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

	def __init__(self,prefix):
		self.prefix = prefix
		self.qfiles = dict()

	def loadQ(self):
		qfn = self.prefix + ".qfiles.json"
		if os.path.isfile(qfn):
			with open(qfn) as fh:
				self.qfiles = json.load(fh)
		else:
			print("ERROR:", qfn, "does not exist.")
			print("Exiting program...")
			raise SystemExit

	def evalAdmix(self, k, K, np):
		qf = self.prefix + "." + str(k) + "_1.Q"
		eAf = self.prefix + "." + str(k) + "_1.corres"
		evalAdmix_str_com = "evalAdmix -plink " + self.prefix + " -fname " + self.prefix + "." + str(k) + "_1.P -qname " + qf + " -o " + eAf + " -P " + str(np)

		call = SysCall(evalAdmix_str_com)
		call.run_program()

	def Rcode(self, funcs, k, K):
	
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
		qscoresf = self.prefix + "." + str(k) + "_1.Q"
		eAf = self.prefix + "." + str(k) + "_1.corres"
		output = eAf + ".png"

		# read in files
		pop = base.as_matrix(utils.read_table(famf))
		q = utils.read_table(qscoresf)
		cor = base.as_matrix(utils.read_table(eAf))

		print(pop)
		print(type(pop))
		print(pop.rx(True,2))
		#print(q)

		# run plotting functions
		ordr = myfunc.orderInds(pop=base.as_vector(pop.rx(True,2)), q=q)
		print(type(ordr))
		print(ordr)

		grdevices.png(file=output)
		myfunc.plotCorRes(cor_mat=cor, pop=base.as_vector(pop.rx(True,2)), ord=ordr, title="test", max_z=0.1, min_z=-0.1)
		grdevices.dev_off()
