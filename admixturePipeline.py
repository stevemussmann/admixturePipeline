#!/bin/env python

from comline import ComLine
from vcf import VCF

import sys



def main():
	input = ComLine(sys.argv[1:])
	vcf_file = VCF(input.args.vcf)
	vcf_file.convert()

main()

raise SystemExit
