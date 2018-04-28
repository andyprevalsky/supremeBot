
import requests
import webbrowser
import time
import re
import sys
from bs4 import BeautifulSoup as bs
from requests.utils import dict_from_cookiejar
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def add_to_cart(size, item, section, color):

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
			time.sleep(1)

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

	#use execute scripts to cutdown time by ~1.2 seconds, but increases likelyhood of bot detection
	
	element = driver.find_element_by_css_selector("input[placeholder='name']")
	element.click()
	element.send_keys(billing_dict['Full_Name'])
	#driver.execute_script("arguments[0].setAttribute('value', arguments[1])", element, billing_dict['Full_Name'])

	element = driver.find_element_by_css_selector("input[placeholder='email']")
	element.click()
	element.send_keys(billing_dict['Email'])
	#driver.execute_script("arguments[0].setAttribute('value', arguments[1])", element, billing_dict['Email'])

	element = driver.find_element_by_css_selector("input[placeholder='tel']")
	element.click()
	element.send_keys(billing_dict['Telephone'])
	#driver.execute_script("arguments[0].setAttribute('value', arguments[1])", element, billing_dict['Telephone'])

	element = driver.find_element_by_css_selector("input[placeholder='address']")
	element.click()
	element.send_keys(billing_dict['Billing_Address'])
	#driver.execute_script("arguments[0].setAttribute('value', arguments[1])", element, billing_dict['Billing_Address'])

	element = driver.find_element_by_css_selector("input[placeholder='zip']")
	element.click()
	element.send_keys(billing_dict['Billing_Zip'])
	#driver.execute_script("arguments[0].setAttribute('value', arguments[1])", element, billing_dict['Billing_Zip'])

	element = driver.find_element_by_css_selector("input[placeholder='city']")
	element.click()
	element.send_keys(billing_dict['Billing_City'])
	#driver.execute_script("arguments[0].setAttribute('value', arguments[1])", element, billing_dict['Billing_City'])

	element = driver.find_element_by_css_selector("input[placeholder='number']")
	element.click()
	element.send_keys(billing_dict['CCN'])
	#driver.execute_script("arguments[0].setAttribute('value', arguments[1])", element, billing_dict['CCN'])

	element = driver.find_element_by_css_selector("input[placeholder='CVV']")
	element.click()
	element.send_keys(billing_dict['Card_CC'])
	#driver.execute_script("arguments[0].setAttribute('value', arguments[1])", element, billing_dict['Card_CC'])
	
	element = driver.find_element_by_id('order_billing_state')
	element.click()
	driver.find_element_by_css_selector("option[value='%s']" % billing_dict['Billing_State']).click()
	#Select(element).select_by_value(billing_dict['Billing_State'])
	
	element = driver.find_element_by_id('credit_card_month')
	element.click()
	driver.find_element_by_css_selector("option[value='%s']" % billing_dict['Card_Month']).click()
	#Select(element).select_by_value(billing_dict['Card_Month'])

	element = driver.find_element_by_id('credit_card_year')
	element.click()
	driver.find_element_by_css_selector("option[value='%s']" % billing_dict['Card_Year']).click()
	#Select(element).select_by_value(billing_dict['Card_Year'])

	driver.find_element_by_xpath(".//*[contains(text(), 'I have read and agree to the')]").click()
	driver.find_element_by_css_selector("input[type='submit']").click()

def server_setup(username, password):
	
	global session

	driver = webdriver.Chrome('/Users/ap/Desktop/chromium/src/out/Default/chromedriver') #chromedriver with $cdc changed
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


	input("Finish Captcha and Submit, Then Press Enter to Run Bot...")

	driver.switch_to_window(supreme_window)
	
	return driver
'''
	global session
	chromeOptions = webdriver.ChromeOptions()
	prefs = {"profile.managed_default_content_settings.javascript":2} #disable javascript to bypass captcha
	chromeOptions.add_experimental_option("prefs",prefs)
	driver = webdriver.Chrome('/Users/ap/Desktop/chromium/src/out/Default/chromedriver', chrome_options=chromeOptions) #chromedriver with $cdc changed
	driver.get("https://www.supremenewyork.com")
	input("Setup Complete, Press Enter to Run Bot...")
	return driver
'''

if __name__ == "__main__":

	billing_dict = {										#fill in with your own billing info
	"Full_Name" : "First Last",
	"Email" : "YourEmail@gmail.com",
	"Telephone" : "999 888 7777",
	"Billing_Address" : "123 Sesame St",
	"Billing_Zip" : "77777",
	"Billing_City" : "Dallas",
	"Billing_State" : "TX",
	"Billing_Country" : "United States",
	"CCN" : "1111 1111 1111 1111",							#input card with spaces every 4 numbers
	"Card_Month" : "01",
	"Card_Year" : "2020",
	"Card_CC" : "123"
	}

	username = "YourEmail@gmail.com"					#fill in with your gmail account
	password = "YourPassword"


	session = requests.session()	
	driver = server_setup(username, password)

	start1_time = time.time() 

	start2_time = time.time() 
	add_to_cart("Large", "Box Logo Hooded Sweatshirt", "sweatshirts", "Pale Lime")			#copy name exactly as said in news, color has first letter captilized, size has first letter capitlized
	print("Add to cart time is  %s seconds " % (time.time() - start2_time))

	start3_time = time.time() 
	add_cookies(driver)
	print("Add cookies time is  %s seconds " % (time.time() - start3_time))

	start4_time = time.time() 
	checkout(driver, billing_dict)
	print("Checkout time is %s seconds " % (time.time() - start4_time))

	print("Total Bot time is %s seconds " % (time.time() - start1_time))

