#!/usr/bin/env python3

from clumpak import Clumpak
from clumpakWeb import ClumpakWeb
from clumpakComline import ComLine

import sys

def main():
	input = ComLine(sys.argv[1:])
	if input.args.web:
		clmpkw = ClumpakWeb(input.args.results, input.args.prefix, input.args.email, input.args.MCL, input.args.DISTRUCT)
	elif input.args.mainpipeline:
		clmpk = Clumpak()
		clmpk.mainP(input.args.results, input.args.prefix, input.args.MCL, input.args.DISTRUCT)
	elif input.args.bestk:
		clmpk = Clumpak()
		clmpk.bestK(input.args.ll)

main()

raise SystemExit
