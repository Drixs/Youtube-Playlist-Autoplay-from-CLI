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
from ConfigParser import SafeConfigParser
from ConfigParser import RawConfigParser

CONFIG_FILE = 'config.ini'

driver = None
wait = None
DEBUG = False

def click_on_element_by_xpath(query):
	submit=wait.until(EC.presence_of_element_located((By.XPATH, query)))
	submit.click()

def get_username():
	parser = SafeConfigParser()
	parser.read(CONFIG_FILE)
	return parser.get('youtube', 'username')

def get_last_session_instnace():
	parser = SafeConfigParser()
	parser.read(CONFIG_FILE)

	if parser.has_section('chromedriver'):
		return parser._sections['chromedriver']
	else:
		None

def set_session_instance(session_url, session_id):
	parser = SafeConfigParser()
	parser.read(CONFIG_FILE)
	if not parser.has_section('chromedriver'):
		parser.add_section('chromedriver')

	parser.set('chromedriver', 'session_url', str(session_url))
	parser.set('chromedriver', 'session_id', str(session_id))
	with open(CONFIG_FILE, "w") as f:
		parser.write(f)


def exit_handler():
	global driver
	driver.quit()

def chrome_driver_new_session():
	# Extension Enable: uBlock
	chrome_options = webdriver.ChromeOptions()
	chrome_options.add_extension('uBlock-Origin_v1.16.18.crx')
	chrome_options.add_argument("--start-minimized") # TODO: Really make it minimze!!!

	print "Initializing new ChromeDriver.."
	args = ["hide_console", ] # Hide chromdriver console. reading required: https://stackoverflow.com/a/48802883
	driver = webdriver.Chrome(chrome_options=chrome_options, service_args=args)

	# set current session data
	session_url = driver.command_executor._url
	session_id = driver.session_id
	set_session_instance(session_url, session_id)

	return driver

def chrome_driver_reuse_session():
	# Try using exising ChromeDriver session, if exists.
	last_session = get_last_session_instnace()

	chrome_options = webdriver.ChromeOptions()
	chrome_options.add_argument("--headless") # make the "new window" that going to open invisible.
	driver = webdriver.Remote(command_executor=last_session['session_url'], desired_capabilities=chrome_options.to_capabilities())

	# Close the "new window" created from webdriver.Remote execution
	driver.close()

	# Reuse the already opened-visible window.
	driver.session_id = last_session['session_id']

	# Should raise exception if it is closed session
	if driver.current_url:
		print "Reuseing existing ChromeDriver.."

	return driver

def validate_args():
	if DEBUG:
		if len(sys.argv) == 1:
			sys.argv = ['D:\\myCustomPath\\youtube-playlist\\play-youtube-playlist-by-name.py', 'Chillout']

	if len(sys.argv) != 2:
		print "Usage: " + os.path.basename(__file__) + " PLAYLIST_NAME"
		exit()
	
def get_search_arg():
	search = sys.argv[1]
	search = search.decode(sys.getfilesystemencoding()).encode('utf-8') # Support unicode filenames	
	return search

def play_playlist_according_to_search(driver, search):
	global wait
	wait = WebDriverWait(driver, 250) # it will wait for 250 seconds an element to come into view, you can change the #value

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

	# UI
	driver.minimize_window();


def main():
	global wait
	global driver

	validate_args()
	search = get_search_arg()

	try:
		driver = chrome_driver_reuse_session()

	except Exception as e:
		driver = chrome_driver_new_session()

	play_playlist_according_to_search(driver, search)

if __name__ == '__main__':
	try:
		main()
	except Exception as e:
		print e