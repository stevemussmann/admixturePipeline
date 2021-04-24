import matplotlib.pyplot
import os
import pandas
import re
import natsort as ns

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
		df.sort_index(axis=1,inplace=True)
		c = df.columns
		#c = sorted(ns.natsorted(c), key=str.isdigit, reverse=True)
		c = natural_sort(c)
		df = df[c]
		print(df)
		fig = matplotlib.pyplot.figure(figsize=(12.8,9.6),dpi=300,frameon=False)
		df.boxplot()
		matplotlib.pyplot.grid(b='None')
		matplotlib.pyplot.xticks(rotation=90)
		fig.savefig(self.output, bbox_inches='tight')

