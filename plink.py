from __future__ import print_function

from popmap import Popmap
from syscall import SysCall

import argparse
import os.path
import subprocess
import sys

class Plink():
	'Class for executing Plink commands'

	def __init__(self,prefix):
		self.prefix = prefix

	def recodeStructure(self):
		plink_str_com = "plink --file " + self.prefix + " --allow-extra-chr 0 --recode structure --out " + self.prefix
		call = SysCall(plink_str_com)
		call.run_program()

	def recodePlink(self):
		plink_command = "plink --file " + self.prefix + " --noweb --allow-extra-chr 0 --recode12 --out " + self.prefix
		call = SysCall(plink_command)
		call.run_program()

	def makeBED(self):
		plink_command = "plink --file " + self.prefix + " --make-bed --out " + self.prefix
		call = SysCall(plink_command)
		call.run_program()
