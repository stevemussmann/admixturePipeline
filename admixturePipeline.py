#!/bin/env python

from comline import ComLine
from vcf import VCF
from admixture import Admixture
from popmap import Popmap

import sys

def main():
	input = ComLine(sys.argv[1:])
	vcf_file = VCF(input.args.vcf, input.args.thin)
	#if input.args.filter == True:
	#	vcf_file.convert_filter()
	#else:
	vcf_file.convert()
	populations = Popmap(input.args.popmap)
	vcf_file.plink()
	vcf_file.print_populations(populations)
	admix_run = Admixture(vcf_file.prefix, input.args.np, input.args.minK, input.args.maxK, input.args.rep, input.args.cv)
	admix_run.admix()
	admix_run.create_zip()
	admix_run.loglik()
	admix_run.print_cv()

main()

raise SystemExit
