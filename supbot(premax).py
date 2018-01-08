
# -*- coding: UTF-8 -*-
import requests
import webbrowser
import time
import re
import sys
from json import dumps
from bs4 import BeautifulSoup as bs
from requests.utils import dict_from_cookiejar
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options

def add_to_cart(size, item, section, color):
    # Check to see how long code runs
    #startTime = time.time()

    # Constants to be used through out code
	global session
	baseUrl1 = "http://www.supremenewyork.com/shop/all"
	x = True

    # Keywords
	productCategory = section
	productKeyword = item
	productStyle = color
	baseUrl2 = '{}/{}'.format(baseUrl1, productCategory)

	while x:
		try:
			response = requests.get(baseUrl2)
			soup = bs(response.text, 'html.parser')
			findProduct = soup.find('a', string=productKeyword)
			findStyle = findProduct.find_next('a', string=productStyle)
			productLink = findStyle.get('href')
			sUrl = '{}{}'.format('http://www.supremenewyork.com', productLink)
			x = False
			print('Link Found!')
		except AttributeError:
			print('loading...')
			x = True
			time.sleep(3)

	productSize = size
	response = session.get(sUrl)
	soup = bs(response.text, 'html.parser')
	sizeTag = soup.find('option', text=productSize)
	sizeContainer = sizeTag.get('value')
	tokenTag = soup.find(attrs={'name' : 'csrf-token'})['content']
	form = soup.find('form', {'action': re.compile('(?<=/shop/)(.*)(?=/add)')})

	payload = {
		'st': tokenTag,
		'commit': 'add to cart',
		's': sizeContainer,
		'utf8': '✓'
	}

	headers = ({
		'User Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36'
		'(KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
		'Accept-Encoding': 'gzip, deflate, sdch, br',
		'Accept-Language': 'en-US,en;q=0.8'
	})
	response = session.post('http://www.supremenewyork.com' + form['action'], data = payload, headers = headers)
	if response.status_code == 200:
		print('Your item was added')

	
def add_cookies(driver):
	global session
	cookies = dict_from_cookiejar(session.cookies)
	for key, value in cookies.items():
	    driver.add_cookie({'name': key, 'value': value, 'domain': "www.supremenewyork.com"})
	driver.get("https://www.supremenewyork.com/checkout")

	return driver

def checkout(driver, billing_dict):
	driver.execute_script("document.getElementById('order_billing_name').setAttribute('value', %s)" % dumps(billing_dict['Full_Name'])) 
	driver.execute_script("document.getElementById('order_email').setAttribute('value', %s)" % dumps(billing_dict['Email']))
	driver.execute_script("document.getElementById('order_tel').setAttribute('value', %s)" % dumps(billing_dict['Telephone']))
	driver.execute_script("document.getElementById('bo').setAttribute('value', %s)" % dumps(billing_dict['Billing_Adress']))
	driver.execute_script("document.getElementById('order_billing_zip').setAttribute('value', %s)" % dumps(billing_dict['Billing_Zip'])) 
	driver.execute_script("document.getElementById('order_billing_city').setAttribute('value', %s)" % dumps(billing_dict['Billing_City']))
	Select(driver.find_element_by_id('order_billing_state')).select_by_value(billing_dict['Billing_State'])
	driver.execute_script("document.getElementById('nnaerb').setAttribute('value', %s)" % dumps(billing_dict['CCN']))
	Select(driver.find_element_by_id('credit_card_month')).select_by_value(billing_dict['Card_Month'])
	Select(driver.find_element_by_id('credit_card_year')).select_by_value(billing_dict['Card_Year'])
	driver.execute_script("document.getElementById('orcer').setAttribute('value', %s)" % dumps(billing_dict['Card_CC']))

	driver.find_element_by_xpath(".//*[contains(text(), 'I have read and agree to the')]").click()
	#driver.find_element_by_css_selector("input[type='submit']").click()

def captcha_setup(username, password):

    global session


    driver.get("https://www.supremenewyork.com")

    
	supreme_window = driver.window_handles[0] 
	driver.execute_script("window.open('https://accounts.google.com/signin/v2/identifier?hl=en&passive=true&continue=https%3A%2F%2Fwww.google.com%2F%3Fgws_rd%3Dssl&flowName=GlifWebSignIn&flowEntry=ServiceLogin', 'new_window')")
	google_window = driver.window_handles[1]
	driver.switch_to_window(google_window)
	driver.find_element_by_css_selector("input[type='email']").send_keys(username)
	driver.find_element_by_css_selector("content[class='CwaK9']").click()
	time.sleep(1.5)
	driver.find_element_by_css_selector("input[type='password']").send_keys(password)
	driver.find_element_by_css_selector("content[class='CwaK9']").click()
	driver.execute_script("window.open('https://www.google.com/recaptcha/api2/demo', 'newer_window')")
	captcha_window = driver.window_handles[2]
	driver.switch_to_window(captcha_window)
	driver.find_element_by_class_name("g-recaptcha").click()
	time.sleep(2)

	if(driver.find_elements_by_css_selector("div[class='rc-imageselect-desc-wrapper']") == 0):
		driver.find_element_by_css_selector("input[type='submit']").click()
		raw_input("Setup Complete, Press Enter to Run Bot...")
	else:
		raw_input("Finish Captcha and Submit, Then Press Enter to Run Bot...")

	driver.switch_to_window(supreme_window)
	
    input("Setup Complete, Press Enter to Run Bot...")
    return driver


if __name__ == "__main__":

	billing_dict = {
	"Full_Name" : "Andy Prevalsky",
	"Email" : "andyprevalsky@yahoo.com",
	"Telephone" : "9008007000",
	"Billing_Adress" : "123 Sesame St",
	"Billing_Zip" : "75063",
	"Billing_City" : "Irving",
	"Billing_State" : "TX",
	"Billing_Country" : "United States",
	"CCN" : "4859106853204971",
	"Card_Month" : "10",
	"Card_Year" : "2021",
	"Card_CC" : "933"
	}

	username = "andyprevalsky1@gmail.com"
	password = "rockey181818"


	session = requests.session()	
	driver = captcha_setup(username, password)

	start1_time = time.time() 

	start2_time = time.time() 
	add_to_cart("Medium", "Hooded Suede Work Jacket", "Jackets", "Tree Camo")
	print("Add to cart time is  %s seconds " % (time.time() - start2_time))

	start3_time = time.time() 
	add_cookies(driver)
	print("Add cookies time is  %s seconds " % (time.time() - start3_time))

	start4_time = time.time() 
	#checkout(driver, billing_dict)
	print("Checkout time is %s seconds " % (time.time() - start4_time))

	print("Total Bot time is %s seconds " % (time.time() - start1_time))

