#!/bin/env python

from comline import ComLine
from vcf import VCF
from admixture import Admixture

import sys



def main():
	input = ComLine(sys.argv[1:])
	vcf_file = VCF(input.args.vcf)
	vcf_file.convert()
	vcf_file.plink(input.args.filter,input.args.window,input.args.advance,input.args.rsquare)
	admix_run = Admixture(vcf_file.prefix, input.args.np, input.args.minK, input.args.maxK, input.args.rep)
	admix_run.admix()

main()

raise SystemExit
