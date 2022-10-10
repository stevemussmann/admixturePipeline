from __future__ import print_function

from collections import defaultdict
from collections import OrderedDict

class Popmap():
	'Class for parsing a popmap'

	def __init__(self, infile):
		#member variables
		self.popmap = OrderedDict()
		self.popnums = defaultdict(int)
	
		try:
			with open(infile, 'r') as f:
				for line in f:
					(key, val) = line.split()
					self.popmap[key] = val #make map of individual->population
		except ValueError:
			print("Too many columns detected in your popmap file.")
			print(infile, "may have spaces in either sample or population names.")
			print("Verify your popmap file is in the correct format and try rerunning.")
			raise SystemExit
	
	def get_plinkList(self, pfile):
		plinkList = list()
		with open(pfile, 'r') as f:
			for line in f:
				tempLine = line.split()
				plinkList.append(tempLine[0])
		return plinkList
	
	# bed is a boolean describing whether a bed file was input (True) or a ped file (False)
	def print_populations(self, filePrefix, bed):
		pfile=""
		if bed == True:
			pfile = filePrefix + ".fam"
		else:
			pfile = filePrefix + ".ped"
		plinkList = self.get_plinkList(pfile)
		self.sort(plinkList)
		popfile = filePrefix + "_pops.txt"
		f = open(popfile, 'w')
		for ind in plinkList:
			try:
				f.write(self.get_pop(ind))
				f.write("\n")
			except TypeError as e:
				print("ERROR in popmap.py: " + str(e))
				print("Attempted to look up " + ind + " in the popmap file, but no record was found.")
				print("Check that all samples in your plink file appear in your popmap.")
				print("If inputting a .bed file, check that the individual sample identifier is in column 1 of your associated .fam file.")
				print("If inputting a .ped file, check that the individual sample identifier is in column 1 of your .ped file.")
				print("")
				raise SystemExit
		f.close()

	def get_pop(self,ind):
		return self.popmap.get(ind)

	def get_list(self):
		return list(self.popmap.keys())

	def sort(self, vcflist):
		newdict = OrderedDict()
		for key in vcflist:
			if key in self.popmap:
				newdict[key] = self.popmap[key]
		self.popmap = newdict
