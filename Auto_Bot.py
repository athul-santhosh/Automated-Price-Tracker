from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

import re
import time

# need to install gecko driver to proceed further

# gecko driver is installed good to go, else install gecko driver and selenium

# Create a class Bot which is going to be the root of the program

class autoBot(object):

	def __init__(self,items):

		# u can use any website of your choice 
		# here  iam scraping amazon india
		
		self.website_url = "https://www.amazon.in/"        
		self.items = items

		self.profile = webdriver.FirefoxProfile()
		self.options = Options()
		self.driver = webdriver.Firefox(firefox_profile = self.profile,
											firefox_options = self.options)
		self.driver.get(self.amazon_url)

	def search_items(self):

		# For this project i would be updating three informations
		# the link of the element that is most common choice
		# the price of the produc in indian rupees
		# the name of the product that is exactly in the description 

		urls = []                                             
		prices =[]
		names = []

		# we search for the first element in the list

		for item in self.items:
			print(f"searching for {item}.")

			self.driver.get(self.amazon_url)

			# here we are going to the amazon's search bar with the help of driver method 
			# find_element_by_id  

			search_input = self.driver.find_element_by_id("twotabsearchtextbox")

			# then we use send_keys() which send the input of what we have passed in the item list,this will search for the item
			search_input.send_keys(item)

			time.sleep(2)

			# now we select the search button using the find_element by_ xpath,and clicking it
			# this produces the result


			search_button = self.driver.find_element_by_xpath('//*[@id="nav-search"]/form/div[2]/div/input')
			search_button.click()
			# once the search results have been produced 
			# we can take the first result , if the program fetches to get
			# first result due to any error or website config the program fetches for the immediate second result
			# this case has to be taken care well , as else it might crash the program right here

			time.sleep(2)

			# In amazon theres is unique identifier for each result called ASIN ,
			# we can extract this using xpath and this ASIN could be used to take us to the next page

			# we try the first input, if we are properly able to fetch ASIN,we store it and if not we use the expect 
			# block to move to the second ASIN finder
			try:

				first_result = self.driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[2]/div/span[3]/div[2]/div[2]')
				asin = first_result.get_attribute('data-asin')
			except:
				pass

			try:
				first_result = self.driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[2]/div/span[3]/div[2]/div[3]')
				asin = first_result.get_attribute('data-asin')
			except:
				pass

			# once we have the ASIN we can navigate to the product page by using the URL


			url = "https://www.amazon.in/dp/" + asin
			#print(url)
			# we use to seperate functions to get the productprice and product name from the url

			price = self.get_product_price(url)
			name = self.get_product_name(url)

			# we append th details of all the products respectively to all the list
			# this list will be later used to update the spreadsheet

			prices.append(price)
			urls.append(url)
			names.append(name)

			# print(name)
			# print(price)
			# print(url)

			time.sleep(2)

		return prices,urls,names
	def get_product_price(self,url):
		self.driver.get(url)
		product_price = None
		# we fetch the product price from the url given by using the find_element_by_id
		# if we are able to retrieve a price properly then its product price is set to that
 		try:
			product_price = self.driver.find_element_by_id("priceblock_ourprice").text
		except:
			pass
		# if the product cannot be tracked down then , the important step is to acknowledge it
		# and to make the program run smoothly without interpreting anything
		# so we pass an message price is not available



		if product_price is None:
			product_price = "Price Not Availabe :("

		else:
			non_decimal = re.compile(r'[^\d.]+')
			product_price = non_decimal.sub('',product_price)
			product_price = "Rs " + product_price
		# if its not then we extract just the price of product from the the page
		# using regular expression

		return product_price



	def get_product_name(self,url):
		self.driver.get(url)
		product_name = None
		try:
			product_name = self.driver.find_element_by_id("productTitle").text
		except:
			pass
		# the same thing goes with product name , if we are able to fetch the name then its set 
		# product name else we acknowledge it

		if product_name is None:
			product_name = "Name not availabe :("

		return product_name

# uncheck this to give a trail run
# items = ["iphone X","Water bottle "]
# a = autoBot(items)
# a.search_items()








