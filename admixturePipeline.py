#!/usr/bin/env python3

from comline import ComLine
from vcf import VCF
from admixture import Admixture
from popmap import Popmap

import sys

def main():
	input = ComLine(sys.argv[1:])
	if input.args.vcf:
		vcf_file = VCF(input.args.vcf, input.args.thin, input.args.maf, input.args.mac, input.args.indcov, input.args.snpcov, input.args.bi, input.args.remove)

	populations = Popmap(input.args.popmap)
	
	#convert to Plink if using .vcf input, then run admixture
	if input.args.vcf:
		vcf_file.compIndLists(populations)
		vcf_file.convert()
		vcf_file.plink()
		vcf_file.print_populations(populations)
		vcf_file.print_individuals(populations)

		admix_run = Admixture(vcf_file.prefix, input.args.np, input.args.minK, input.args.maxK, input.args.rep, input.args.cv)

	#else if using plink input, go directly to running admixture
	else:
		#print_populations function in popmap class mimics output of print_populations function in vcf class
		populations.print_populations(input.args.plink)
		admix_run = Admixture(input.args.plink, input.args.np, input.args.minK, input.args.maxK, input.args.rep, input.args.cv)
	admix_run.admix()
	admix_run.create_zip()

main()

raise SystemExit
