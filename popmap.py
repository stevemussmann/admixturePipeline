from __future__ import print_function

from collections import defaultdict

class Popmap():
	'Class for parsing a popmap'

	def __init__(self, infile):
		#member variables
		self.popmap = dict()
		self.popnums = defaultdict(int)
		
		data = open(infile, 'r')
		content = data.readlines()
		data.close()

		content = [x.rstrip('\n') for x in content]

		for line in content:
			temp = line.split()
			self.popmap[temp[0].strip('\t\n\r')] = temp[1].strip('\t\n\r') #make map of individual->population

	def get_pop(self,ind):
		return self.popmap.get(ind)
