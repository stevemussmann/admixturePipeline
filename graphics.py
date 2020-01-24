import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot
import os

class Graphics():
	'Class to print plots of data'

	def __init__(self,data,fname):
		self.data = data
		self.output = os.path.splitext(fname)[0] + ".png"


	def printFigure(self):
		data_to_plot = self.prepData()

		fig = matplotlib.pyplot.figure(1, figsize=(18,12))		
		ax = fig.add_subplot(111)
		bp=ax.boxplot(data_to_plot)
		fig.savefig(self.output, bbox_inches='tight')

	def prepData(self):
		lists = list()
		for k,v in self.data.items():
			templist = list()
			for item in v:
				templist.append(float(item))
			lists.append(templist)

		return lists
