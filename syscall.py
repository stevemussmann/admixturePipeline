from __future__ import print_function

import argparse
import os.path
import subprocess
import sys

class SysCall():
	'Class for executing system calls'

	def __init__(self,string):
		self.command = string

	def runCode(self, writeOut, fn="none"):
		process = subprocess.Popen(self.command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
		output, err = process.communicate()
		if writeOut is True:
			f = open(fn, 'wb')
			f.write(output)
			f.close()
		print(err.decode())
		return process.returncode

	def run_program(self):
		print(self.command)
		try:
			ret = self.runCode(False)
			if ret != 0:
				print("Non-zero exit status:")
				print(ret)
				raise SystemExit
		except (KeyboardInterrupt, SystemExit):
			raise
		except:
			print("Unexpected error:")
			print(sys.exc_info())
			raise SystemExit

	def run_admixture(self,prefix,i,j):
		print(self.command)
		try:
			fn = prefix + "." + str(i) + "_" + str(j) + ".stdout" #make name for stdout log file
			ret = self.runCode(True, fn)
			if ret !=0:
				print("Non-zero exit status:")
				print(ret)
				raise SystemExit
		except (KeyboardInterrupt, SystemExit):
			raise
		except:
			print("Unexpected error:")
			print(sys.exc_info())
			raise SystemExit
