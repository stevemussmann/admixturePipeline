from __future__ import print_function

from collections import defaultdict
from collections import OrderedDict

class Popmap():
	'Class for parsing a popmap'

	def __init__(self, infile):
		#member variables
		self.popmap = OrderedDict()
		self.popnums = defaultdict(int)
		
		with open(infile, 'r') as data:
			content = data.read().splitlines()

		for line in content:
			temp = line.split()
			self.popmap[temp[0]] = temp[1] #make map of individual->population

	def get_pop(self,ind):
		return self.popmap.get(ind)

	def get_list(self):
		return list(self.popmap.keys())
