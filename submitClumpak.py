#!/usr/bin/python

from clumpak import Clumpak
from clumpakComline import ComLine

import sys

def main():
	input = ComLine(sys.argv[1:])
	clmpk = Clumpak(input.args.results, input.args.prefix, input.args.email)

main()

raise SystemExit
