#!/usr/bin/env python3

from cvComline import ComLine
from cv import CV
from loglikelihood import LogLikelihood
from graphics import Graphics
from stats import CVStats

import sys



def main():
	input = ComLine(sys.argv[1:])
	cvFile = CV(input.args.cv)
	cvFile.readText() #reads major clusters
	cvFile.readMinor()
	#cvFile.printText()

	logLike = LogLikelihood(input.args.ll)
	logLike.readText() #reads major clusters
	logLike.readMinor()
	#logLike.printText()

	so = CVStats(cvFile.d,input.args.out)
	so.calcStats()
	so.printStats()

	llo = CVStats(logLike.d,input.args.llout)
	llo.calcStats()
	llo.printStats()

	cvPlot = Graphics(cvFile.d,input.args.cv)
	cvPlot.printFigure()
	
	llPlot = Graphics(logLike.d,input.args.ll)
	llPlot.printFigure()

main()

raise SystemExit
