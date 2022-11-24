from collections import defaultdict
from decimal import *

import os
import re

class LogLikelihood():

	def __init__(self, f):
		self.infile = f
		self.d = defaultdict(list)
		self.alld = defaultdict(list)

	def printLoglike(self):
		fh = open("ll_all.txt", "w")
		for k, l in self.alld.items():
			for item in l:
				fh.write(str(k))
				fh.write("\t")
				fh.write(str(item))
				fh.write("\n")
		fh.close()

	def readText(self):
		content = list()
		with open(self.infile, 'r') as fh:
			content = fh.read().splitlines()
		self.parseText(content)

	def parseText(self, lines):
		counter=0
		for line in lines:
			templist = line.split()
			if templist[-1] != "-nan":
				val = Decimal(templist[-1])
				knum = templist[0]
				self.d[knum].append(val)
				self.alld[knum].append(val)
			else:
				print("Warning: -NaN value found for a Loglikelihood value.")

	def readMinor(self):
		path = os.getcwd()
		files = os.listdir(path)
		for f in files:
			if f.startswith("loglikelihood_file.MinClust.K"):
				temp = f.split(".")
				knum = temp[2].replace("K","")
				justk = str(knum)
				knum = str(knum) + ".MinClust." + temp[3]
				content = list()
				with open(f, 'r') as fh:
					content = fh.read().splitlines()
				for line in content:
					temp = line.split().pop(-1)
					if temp != "-nan":
						val = Decimal(temp)
						self.d[knum].append(val)
						self.alld[justk].append(val)
					else:
						print("Warning: -NaN value found for a Loglikelihood value.")

	def printText(self):
		print(self.d)
