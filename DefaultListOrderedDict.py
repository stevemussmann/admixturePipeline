from collections import OrderedDict

class DefaultListOrderedDict(OrderedDict):
	'Class for creating an odereddict with lists as default values'

	def __missing__(self, k):
		self[k] = []
		return self[k]
