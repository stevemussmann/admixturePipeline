from __future__ import print_function

from collections import defaultdict
from decimal import *

import re

class CV():
	'Class for operating on cross-validation values from admixture'
	
	def __init__(self, f):
		self.infile = f
		self.d = defaultdict(list)

	def readText(self):
		content = list()
		with open(self.infile, 'r') as fh:
			content = fh.readlines()
		self.parseText(content)

	def parseText(self, lines):
		for line in lines:
			#print(line)
			val = Decimal(line.strip().split().pop(-1)) #get the cv value for the line
			match = re.search(r'(?P<kval>(K=\d+))', line) #regex to find kval
			knum = int(match.group('kval').split('=').pop(-1)) #get the k-value for the line
			self.d[knum].append(val) #append to dictionary of lists

	def printText(self):
		print(self.d)
