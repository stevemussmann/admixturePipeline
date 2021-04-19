#!/usr/bin/env python3

from cvComline import ComLine
from cv import CV
from graphics import Graphics
from stats import CVStats

import sys



def main():
	input = ComLine(sys.argv[1:])
	cvFile = CV(input.args.cv)
	cvFile.readText()
	cvFile.readMinor()
	#cvFile.printText()

	so = CVStats(cvFile.d,input.args.out)
	so.calcStats()
	so.printStats()

	plot = Graphics(cvFile.d,input.args.cv)
	plot.printFigure()

main()

raise SystemExit
