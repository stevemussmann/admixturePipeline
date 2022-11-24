import os
import sys

from datetime import datetime

from syscall import SysCall

class Clumpak():
	'Class for automated submission of AdmixPipe output to local CLUMPAK installation'

	def __init__(self):
		# test if advanced options need to be used
		self.advanced = False

	def mainP(self,results,prefix,mcl,distruct):
		#if mcl != 1.0 or distruct != 1.0:
		if( bool(mcl) == True) or (bool(distruct) == True):
			self.advanced = True

		# get time in milliseconds to name the run
		date = datetime.utcnow() - datetime(1970, 1, 1)
		ms = str(round(date.total_seconds()*1000))

		# get name of populations file
		p = prefix + "_pops.txt"

		commStr = "CLUMPAK.pl --id " + ms + " --dir clumpakOutput --file " + results + " --inputtype admixture --indtopop " + p

		if self.advanced == True:
			commStr = self.advancedOptions(mcl,distruct,commStr)

		call = SysCall(commStr)
		call.run_program()

	def bestK(self,ll):
		
		# get time in milliseconds to name the run
		date = datetime.utcnow() - datetime(1970, 1, 1)
		ms = str(round(date.total_seconds()*1000))

		commStr = "BestKByEvanno.pl --id " + ms + " --d clumpakBestK --f " + ll + " --inputtype lnprobbyk"

		call = SysCall(commStr)
		call.run_program()

	def advancedOptions(self,mcl,distruct,s):

		if(bool(mcl) == True) and (mcl <=0.99) and (mcl >= 0):
			s = s + " --mclthreshold " + str(mcl)
		elif(bool(mcl) == True) and ((mcl > 0.99) or (mcl < 0)):
			print("User-defined MCL input for advanced options is invalid.")
			print("MCL must be between 0 and 0.99")
			print("Your MCL value was " + str(mcl))
			print("")
			raise SystemExit

		if(bool(distruct) == True) and (distruct <=0.95) and (distruct >= 0):
			s = s + " --mclminclusterfraction " + str(distruct)
		elif(bool(distruct) == True) and ((distruct > 0.95) or (distruct < 0)):
			print("User-defined DISTRUCT threshold for advanced options is invalid.")
			print("Value must be between 0 and 0.95")
			print("Your value was " + str(distruct))
			print("")
			raise SystemExit

		return s
