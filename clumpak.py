import os
import selenium
import sys

from selenium.webdriver import Firefox

class Clumpak():
	'Class for automated submission of AdmixPipe output to CLUMPAK'

	def __init__(self,results,prefix,email):
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

		# submit results file
		popSubmit = driver.find_element_by_name("populations_file")
		popSubmit.send_keys(popPath)

		# submit email address
		emailBox = driver.find_element_by_name("inputEmail")
		emailBox.send_keys(email)

		# submit form
		driver.find_element_by_xpath("//input[@value='Submit Form']").click()
