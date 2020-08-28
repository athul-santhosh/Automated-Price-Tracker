from Auto_Bot import autoBot
import gspread
from oauth2client.service_account import ServiceAccountCredentials

class PriceUpdater(object):

	def __init__(self):

		# these are the various coloums we are going to update in the spread sheet

		self.item_col = 1
		self.price_col = 2
		self.frequency_col = 3
		self.url_col = 4
		self.product_name_col = 5

		# what does scope actually do ?
		# scope authorises permission to client(whoever is authorised) to access all the required files 
		# we need oauth2client module for scope to function properly
		scope = ['https://spreadsheets.google.com/feeds',
		          'https://www.googleapis.com/auth/drive']

		

		# here we pass the client key of google spread sheet
		# this is the pivot step which gives the holder of the key to read and write data to
		# from the spreadsheet, in place of x , should pass the Json key file


		creds = ServiceAccountCredentials.from_json_keyfile_name('x',scope) 
		# we take the access to creds fromt the key

		client = gspread.authorize(creds) 
		# client is authorized to the spreadsheet object which can read and write the spread sheet

		self.sheet = client.open('ProductPrice').sheet1  
		# we create another object sheet which will help us to manipulate the data
		# we need to specify which sheet we are going to use thus, we also pass the sheet number

	def process_item_list(self):

		# this is the important step in which we extract the values from the first list of the spead sheet
		# this is were the user inputs items one by one
		# we are going to extrac each items one by one ignoring the except the first row

		items = self.sheet.col_values(self.item_col)[1:] 

		# so now we have a items which contains the list of all the elements we need to search for in the 
		# website
		# col_values is a method to extract he same data

		search_bot = autoBot(items)
		# we create an object for autoBot program 

		prices,urls,names = search_bot.search_items()
		# we recieve all the values from the autoBot(the scraping program) for prices ,urls and names ,
		# this is the data that is returned by the auto Bot program

		print("updating the spreadsheet")

		for i in range(len(prices)):
			# here we update the prices of the various columns respectively for each items,
			# all details have been prefetched by autoBot
			self.sheet.update_cell(i+2,self.price_col,prices[i])
			self.sheet.update_cell(i+2,self.url_col,urls[i])
			self.sheet.update_cell(i+2,self.product_name_col,names[i])

# object for PriceUpdater
price_updater = PriceUpdater()
# function call
price_updater.process_item_list()