#!/usr/bin/env python3

from evalAdmixComline import ComLine
from distruct import Distruct
from clumpp import Clumpp

import subprocess
import sys

from rpy2.robjects import StrVector
from rpy2.robjects.packages import STAP
from rpy2.robjects.packages import importr
from rpy2.robjects import r

def runCode(string):
	process = subprocess.Popen(string, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
	output, err = process.communicate()
	print(err.decode())
	return process.returncode

def run_program(string):
	print(string)
	try:
		ret = runCode(string)
		if ret != 0:
			print("Non-zero exit status:")
			print(process.returncode)
			raise SystemExit
	except (KeyboardInterrupt, SystemExit):
		raise
	except:
		print("Unexpected error:")
		print(sys.exc_info())
		raise SystemExit

def plink(fprefix):
	plink_str_com = "plink --file " + fprefix + " --make-bed --out " + fprefix
	run_program(plink_str_com)

def evalAdmix(fprefix, k, np):
	qf = fprefix + "." + str(k) + "_1.Q"
	eAf = fprefix + "." + str(k) + "_1.corres"
	evalAdmix_str_com = "evalAdmix -plink " + fprefix + " -fname " + fprefix + "." + str(k) + "_1.P -qname " + qf + " -o " + eAf + " -P " + str(np)
	run_program(evalAdmix_str_com)

def fixFam(popmap, fprefix):
	#get name for .fam file
	famf = fprefix + ".fam"

	#read popmap into dict
	d=dict()
	with open(popmap, 'r') as f:
		for line in f:
			(key, val) = line.split()
			d[key] = val

	fam=list()
	with open(famf, 'r') as f:
		for line in f:
			temp = line.split()
			temp[1] = d[temp[0]]
			newline=' '.join(temp)
			fam.append(newline)

	print(fam)

	with open(famf, 'w') as fh:
		for line in fam:
			fh.write('%s\n' % line)


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

	# make plink .bed file
	plink(input.args.prefix)
	fixFam(input.args.popmap, input.args.prefix)
	evalAdmix(input.args.prefix, input.args.testK, input.args.np)
	Rcode(input.args.evalAdmixRcode, input.args.prefix, input.args.testK)


	

main()

raise SystemExit
