#!/usr/bin/env python3

from evalAdmixComline import ComLine
from syscall import SysCall
from plink import Plink

from rpy2.robjects import StrVector
from rpy2.robjects.packages import STAP
from rpy2.robjects.packages import importr
from rpy2.robjects import r

import sys

def evalAdmix(fprefix, k, np):
	qf = fprefix + "." + str(k) + "_1.Q"
	eAf = fprefix + "." + str(k) + "_1.corres"
	evalAdmix_str_com = "evalAdmix -plink " + fprefix + " -fname " + fprefix + "." + str(k) + "_1.P -qname " + qf + " -o " + eAf + " -P " + str(np)

	call = SysCall(evalAdmix_str_com)
	call.run_program()

def Rcode(funcs, fprefix, k):
	
	# import R functions
	utils = importr('utils')
	base = importr('base')
	grdevices = importr('grDevices')

	# import R plotting functions from evalAdmix
	with open(funcs, 'r') as f:
		string = f.read()
	myfunc = STAP(string, "myfunc")

	#make file names
	famf = fprefix + ".fam"
	qscoresf = fprefix + "." + str(k) + "_1.Q"
	eAf = fprefix + "." + str(k) + "_1.corres"
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


def main():
	input = ComLine(sys.argv[1:])

	# make plink .bed file and fix .fam file
	pl = Plink(input.args.prefix)
	pl.makeBED()
	pl.fixFam(input.args.popmap)

	evalAdmix(input.args.prefix, input.args.testK, input.args.np)
	Rcode(input.args.evalAdmixRcode, input.args.prefix, input.args.testK)


	

main()

raise SystemExit
