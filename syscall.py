from __future__ import print_function

import argparse
import os.path
import subprocess
import sys

class SysCall():
	'Class for executing system calls'

	def __init__(self,string):
		self.command = string

	def runCode(self):
		process = subprocess.Popen(self.command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
		output, err = process.communicate()
		print(err.decode())
		return process.returncode

	def run_program(self):
		print(self.command)
		try:
			ret = self.runCode()
			if ret != 0:
				print("Non-zero exit status:")
				print(process.returncode)
				raise SystemExit
		except (KeyboardInterrupt, SystemExit):
			raise
		except:
			print("Unexpected error:")
			print(sys.exc_info())
			raise SystemExit
