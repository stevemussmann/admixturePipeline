import os
import shutil
import sys
import json

from datetime import datetime

from syscall import SysCall

class Clumpak():
	'Class for automated submission of AdmixPipe output to local CLUMPAK installation'

	def __init__(self):
		# test if advanced options need to be used
		self.mclOpt = False
		self.distructOpt = False

		# load args from admixturePipeline.py
		self.apArgs = dict()
		with open('admixturePipeline.json') as f:
			self.apArgs = json.load(f)

	def mainP(self,results,prefix,mcl,distruct):
		if bool(mcl) == True:
			self.mclOpt = True
		
		if bool(distruct) == True:
			self.distructOpt = True

		# obtain number of replicates performed per K in admixturePipeline.py
		reps = self.apArgs['rep']

		# get time in milliseconds to name the run
		date = datetime.utcnow() - datetime(1970, 1, 1)
		ms = str(round(date.total_seconds()*1000))

		# get name of populations file
		p = prefix + "_pops.txt"

		# check if output directory already exists and delete if it does
		directory = "clumpakOutput"
		self.deleteDir(directory)

		commStr = "CLUMPAK.pl --id " + ms + " --dir " + directory + " --file " + results + " --inputtype admixture --indtopop " + p

		if self.mclOpt == True:
			commStr = self.mclOption(mcl,commStr)
		
		if self.distructOpt == True:
			commStr = self.distructOption(distruct,commStr)
		else:
			commStr = self.distructDefault(commStr,reps)

		call = SysCall(commStr)
		call.run_program()

	def bestK(self,ll):
		
		# get time in milliseconds to name the run
		date = datetime.utcnow() - datetime(1970, 1, 1)
		ms = str(round(date.total_seconds()*1000))
		
		# check if output directory already exists and delete if it does
		directory = "clumpakBestK"
		self.deleteDir(directory)

		commStr = "BestKByEvanno.pl --id " + ms + " --d " + directory + " --f " + ll + " --inputtype lnprobbyk"

		call = SysCall(commStr)
		call.run_program()

	def mclOption(self,mcl,s):

		if(bool(mcl) == True) and (mcl <=0.99) and (mcl >= 0):
			s = s + " --mclthreshold " + str(mcl)
		elif(bool(mcl) == True) and ((mcl > 0.99) or (mcl < 0)):
			print("User-defined MCL input for advanced options is invalid.")
			print("MCL must be between 0 and 0.99")
			print("Your MCL value was " + str(mcl))
			print("")
			raise SystemExit

		return s

	def distructOption(self,distruct,s):
		if(bool(distruct) == True) and (distruct <=0.95) and (distruct >= 0):
			s = s + " --mclminclusterfraction " + str(distruct)
		elif(bool(distruct) == True) and ((distruct > 0.95) or (distruct < 0)):
			print("User-defined DISTRUCT threshold for advanced options is invalid.")
			print("Value must be between 0 and 0.95")
			print("Your value was " + str(distruct))
			print("")
			raise SystemExit
		return s

	def distructDefault(self,s,reps):
		calcVal = 1/reps
		s = s + " --mclminclusterfraction " + str(calcVal)
		return s

	def deleteDir(self,directory):
		if os.path.exists(directory):
			shutil.rmtree(directory)
