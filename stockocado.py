## TODO

## [x] 1. Price Retriever
## [o] 2. Price Listner
## [ ] 3. Price Grapher/Processer
##          [ ] Timestamps?
## [ ] 4. Buy/Sell decision
## [o] 5. Thread 1-4 for multiple stocks

import threading
from bs4 import BeautifulSoup
import urllib
import time
from time import gmtime, strftime
from filelock import FileLock

class Stockocado():
	global VALUE, TIME, MONTH, DAY_LOW, DAY_HIGH
	VALUE = 0
	TIME = 1
	MONTH = 2
	DAY_LOW = 3
	DAY_HIGH = 4
	global symbol


	def read_symbols(self):
		index_array = [line.rstrip('\n') for line in open('symbols.txt')]
		return index_array

	def __init__(self):
		symbols = self.read_symbols()
		for index in range(len(symbols)):	
			threading.Thread(target=self._listener, args=(symbols[index],)).start()

	def _listener(i, index):
		print 'listener started on: ' + index
		i.symbol = index			
		f = open('my_' + index, 'a')
		f.write('0')
		f.close()

		f = open('bank', 'a')
		f.write('10000000')
		f.close()

		while(True):
			# Get information
			quote = i.get_quote(index)

			# Print to console
			value = quote[VALUE]
			value = str(round(value,2))
			timestamp = quote[TIME]
			# print '[ ' + index + ' ] ' + value

			# Save information
			# f = open(index, 'a')
			# f.write( timestamp + '\n')
			# f.write(value + '\n')
			# f.close()

			# Send to decide if buy/sell
			i.process(quote)

			time.sleep(1)

	def get_quote(self, index):
		page = urllib.urlopen('http://markets.siliconinvestor.com/siliconinvestor/quote?Symbol=' + index)
		# GET TIME
		timestamp = strftime("%Y-%m-%d %H:%M:%S", gmtime())
		soup = BeautifulSoup(page, "html.parser")

		# GET VALUE
		value_div = soup.find(id='quotenav1_field_price')
		value = float(value_div.contents[0][:])

		# GET MONTH PERFORMANCE
		month = soup.find(id='quotenav1_field_price')
		month = float(month.contents[0][:])

		# GET LOW FOR DAY
		day_low = soup.find(id='quotenav1_field_price')
		day_low = float(day_low.contents[0][:])

		# GET HIGH FOR DAY
		day_high = soup.find(id='quotenav1_field_price')
		day_high = float(day_high.contents[0][:])

		return value, timestamp, month, day_low, day_high


	def process(self, quote):
		# IF THE STOCK IS DOING BAD LONG-RUN LEAVE IT ALONE
		# if (month_performance < 0):
		#	return

		# BUY WHEN LOW
		if (quote[VALUE] < quote[DAY_LOW]):
			buy(quote)

		# SELL WHEN HIGH
		if (quote[VALUE] > quote[DAY_HIGH]):
			sell(quote)

	def buy(self, quote):
		# What is $1,000 of shares?
		shares = 1000 / value

		# open my_SYMBOL
		f = open('my_' + self.symbol, 'w')
		existing_shares = int(f.readlines())
		# add X shares		
		existing_shares = existing_shares + shares
		f.write(existing_shares)
		f.close()

		# open bank
		with FileLock("bank"):
			f = open('bank', 'a')
			# take out $1000 for X shares		
			new_balance = int(f.readlines()) - 1000
			f.write(new_balance)
			f.close()

		print 'Bought ' + self.symbol + '. ' + str(shares) + ' shares.'

		# wait 5 minutes before doing another trade
		time.sleep(60*5) 

	def sell(self, quote):
		# open my_SYMBOL
		f = open('my_' + self.symbol, 'w')
		# How many shares do we have?		
		existing_shares = int(f.readlines())
		f.write('0')
		f.close()

		# open bank
		with FileLock("bank"):
			f = open('bank', 'a')
			# add value for for X shares		
			new_balance = int(f.readlines()) + (existing_shares * quote[VALUE])
			f.write(new_balance)
			f.close()

		print 'Sold ' + self.symbol + '. New balance: ' + str(new_balance)


s = Stockocado()

## Should the mather-s be in a different file? a: no i hate python