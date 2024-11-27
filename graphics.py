import pandas
import matplotlib.pyplot
import os
import re

def natural_sort(l): 
	convert = lambda text: int(text) if text.isdigit() else text.lower() 
	alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
	return sorted(l, key = alphanum_key)

class Graphics():
	'Class to print plots of data'

	def __init__(self,data,fname):
		self.data = data
		self.output = os.path.splitext(fname)[0] + ".png"


	def printFigure(self):
		#make pandas dataframe to include NaN values
		df = pandas.DataFrame(dict([ (k,pandas.Series(v)) for k,v in self.data.items() ]), dtype=float)
		# get columns for sorting; sort them; then apply back to dataframe
		c = df.columns
		c = natural_sort(c)
		df = df[c]

		print(df)
		fig = matplotlib.pyplot.figure(figsize=(12.8,9.6),dpi=300,frameon=True)
		df.boxplot()
		matplotlib.pyplot.xticks(rotation=90)
		matplotlib.pyplot.grid(visible=None,axis='both',which='major')
		fig.savefig(self.output, bbox_inches='tight')

