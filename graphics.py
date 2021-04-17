import matplotlib.pyplot
import os
import pandas

class Graphics():
	'Class to print plots of data'

	def __init__(self,data,fname):
		self.data = data
		self.output = os.path.splitext(fname)[0] + ".png"


	def printFigure(self):
		#make pandas dataframe to include NaN values
		df = pandas.DataFrame(dict([ (k,pandas.Series(v)) for k,v in self.data.items() ]), dtype=float)
		print(df)
		fig = matplotlib.pyplot.figure(figsize=(12.8,9.6),dpi=300,frameon=False)
		df.boxplot()
		fig.savefig(self.output, bbox_inches='tight')
