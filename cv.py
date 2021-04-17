from __future__ import print_function

from collections import defaultdict
from decimal import *

import os
import re

class CV():
	'Class for operating on cross-validation values from admixture'
	
	def __init__(self, f):
		self.infile = f
		self.d = defaultdict(list)

	def readText(self):
		content = list()
		with open(self.infile, 'r') as fh:
			content = fh.read().splitlines()
		self.parseText(content)

	def parseText(self, lines):
		counter=0
		for line in lines:
			val = Decimal(line.split().pop(-1)) #get the cv value for the line
			match = re.search(r'(?P<kval>(K=\d+))', line) #regex to find kval
			knum = match.group('kval').split('=').pop(-1) #get the k-value for the line
			self.d[knum].append(val) #append to dictionary of lists

	def readMinor(self):
		path = os.getcwd()
		files = os.listdir(path)
		for f in files:
			if f.startswith("cv_file.MinClust.K"):
				temp = f.split(".")
				knum = temp[2] + ".MinClust." + temp[3]
				knum = knum.replace("K","")
				content = list()
				with open(f, 'r') as fh:
					content = fh.read().splitlines()
				for line in content:
					val = Decimal(line.split().pop(-1))
					match = re.search(r'(?P<kval>(K=\d+))', line) #regex to find kval
					self.d[knum].append(val)

	def printText(self):
		print(self.d)
