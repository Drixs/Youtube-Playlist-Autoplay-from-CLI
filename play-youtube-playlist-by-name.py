# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import sys
import urllib
import os
import codecs
import atexit
from ConfigParser import SafeConfigParser

driver = None
wait = None

def click_on_element_by_xpath(query):
	submit=wait.until(EC.presence_of_element_located((By.XPATH, query)))
	submit.click()

def get_username():
	parser = SafeConfigParser()
	parser.read('config.ini')
	return parser.get('youtube', 'username')

def exit_handler():
	global driver
	driver.quit()

def main():
	global wait
	global driver

	search = sys.argv[1]
	search = search.decode(sys.getfilesystemencoding()).encode('utf-8') # Support unicode filenames

	# Extension Enable: uBlock
	chop = webdriver.ChromeOptions()
	chop.add_extension('uBlock-Origin_v1.16.18.crx')

	# Open Browser
	args = ["hide_console", ] # https://stackoverflow.com/a/48802883
	driver = webdriver.Chrome(chrome_options = chop, service_args=args)

	# Close browser instance, if our python closed.
	atexit.register(exit_handler)

	# Hide console
	wait = WebDriverWait(driver,250) # it will wait for 250 seconds an element to come into view, you can change the #value
	
	# Browse YOUTUBE playlist search
	url = "https://www.youtube.com/user/{}/search?query={}".format(get_username(), urllib.quote(search))
	driver.get(url)

	# Click on playlist named what we've searched..
	query = """//*[@id="video-title" and contains(text(), {})]""".format(search)
	click_on_element_by_xpath(query)

	# Click on LOOP option, and Shuffle
	query = """//*[@id="button" and @aria-label="Loop playlist"]"""
	click_on_element_by_xpath(query)
	query = """//*[@id="button" and @aria-label="Shuffle playlist"]"""
	click_on_element_by_xpath(query)


	# Forward
	query = """//*[@class="ytp-next-button ytp-button"]"""
	click_on_element_by_xpath(query)

	# Close script in case of browser manually closed
	try:
		while driver.current_url:
			pass
	except:
		exit()

if __name__ == '__main__':
	try:
		main()
	except Exception as e:
		print e