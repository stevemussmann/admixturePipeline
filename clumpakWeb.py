import os
import selenium
import sys

from selenium.webdriver import Firefox
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class ClumpakWeb():
	'Class for automated submission of AdmixPipe output to CLUMPAK web server'

	def __init__(self,results,prefix,email,mcl,distruct):
		# test if advanced options need to be used
		self.advanced = False
		#if mcl != 1.0 or distruct != 1.0:
		if( bool(mcl) == True) or (bool(distruct) == True):
			self.advanced = True

		# get path to results file
		resultsPath = os.path.join(os.getcwd(),results)

		# get path to pops file
		p = prefix + "_pops.txt"
		popPath = os.path.join(os.getcwd(),p)

		# open Firefox
		driver = Firefox()
		driver.implicitly_wait(0.5)
		driver.maximize_window()

		# get clumpak webpage
		driver.get('http://clumpak.tau.ac.il/')

		# submit results file
		resultsSubmit = driver.find_element_by_name("structureZipFile")
		resultsSubmit.send_keys(resultsPath)

		# select admixture
		driver.find_element_by_xpath("//input[@value='admixture']").click()

		# submit populations file
		popSubmit = driver.find_element_by_name("populations_file")
		popSubmit.send_keys(popPath)

		# click "Advanced Options
		if self.advanced == True:
			self.advancedOptions(driver,mcl,distruct)
		#driver.find_element_by_xpath("//input[@value='Advanced Options']").click()

		# submit email address
		emailBox = driver.find_element_by_name("inputEmail")
		emailBox.send_keys(email)

		# submit form
		driver.find_element_by_xpath("//input[@value='Submit Form']").click()
	
	def advancedOptions(self,driver,mcl,distruct):
		advancedMCL = False
		advancedDistruct = False

		if(bool(mcl) == True) and (mcl <=0.99) and (mcl >= 0):
			advancedMCL = True
		elif(bool(mcl) == True) and ((mcl > 0.99) or (mcl < 0)):
			print("User-defined MCL input for advanced options is being ignored.")
			print("MCL must be between 0 and 0.99")
			print("Your MCL value was " + str(mcl))
			print("")

		if(bool(distruct) == True) and (distruct <=0.95) and (distruct >= 0):
			advancedDistruct = True
		elif(bool(distruct) == True) and ((distruct > 0.95) or (distruct < 0)):
			print("User-defined DISTRUCT threshold for advanced options is being ignored.")
			print("Value must be between 0 and 0.95")
			print("Your value was " + str(distruct))
			print("")

		if(advancedMCL == True) or (advancedDistruct == True):
			driver.find_element_by_xpath("//input[@value='Advanced Options']").click()
			driver.implicitly_wait(0.5)
			#body = driver.find_element_by_css_selector('body')
			#body.send_keys(Keys.PAGE_DOWN)

		if advancedMCL == True:
			print(mcl)
			driver.find_element_by_xpath("//input[@type='radio' and @name='MCL_type' and @value='UserDefined']").click()
			mclBox = driver.find_element_by_xpath("//input[@id='MCL_threshold' and @type='number' and @name='MCL_threshold']")
			mclBox.clear()
			mclBox.send_keys(str(mcl))
			#element=WebDriverWait(driver, 10).until(expected_conditions.element_to_be_clickable((By.XPATH, "//input[@name='MCL_threshold']")))
			#element.location_once_scrolled_into_view
			#element.click()
		if advancedDistruct == True:
			print(distruct)
			driver.find_element_by_xpath("//input[@type='radio' and @name='MCL_MinClusterFraction_radioBtn' and @value='UserDefined']").click()
			distructBox = driver.find_element_by_xpath("//input[@id='MCL_MinClusterFraction_threshold' and @type='number' and @name='MCL_MinClusterFraction_threshold']")
			distructBox.clear()
			distructBox.send_keys(str(distruct))
		
