import threading
from bs4 import BeautifulSoup
import urllib
import time
from time import gmtime, strftime
from filelock import FileLock

class Stockocado():
	global VALUE, TIME, MONTH, DAY_LOW, DAY_HIGH, symbol, toggle
	VALUE = 0
	TIME = 1
	MONTH = 2
	DAY_LOW = 3
	DAY_HIGH = 4
	toggle = 0

	def read_symbols(self):
		symbol_array = [line.rstrip('\n') for line in open('symbols.txt')]
		return symbol_array

	def __init__(self):
		# Get symbols of stocks to watch (CRM, NTFX, GOOG, etc.)
		symbols = self.read_symbols()

		# put some dolla dolla in that pocket
		f = open('bank', 'w')
		f.write('10000000')
		f.close()

		# each symbol gets their own thread
		for symbol in range(len(symbols)):	
			threading.Thread(target=self._listener, args=(symbols[symbol],)).start()

	def _listener(i, symbol):
		# DEBUG OFF i.toggle = 0
		print 'listener started on: ' + symbol
		i.symbol = symbol		

		# Keep track of how many shares you have	
		f = open('my_' + symbol, 'w')
		f.write('0')
		f.close()

		while(True):
			# Get information (value, timestamp, monthly performance, current day high, current day low)
			quote = i.get_quote(symbol)

			# Print to console
			value = quote[VALUE]
			value = str(round(value,2))
			timestamp = quote[TIME]
			# print '[ ' + symbol + ' ] ' + value

			# Save information
			# f = open(symbol, 'a')
			# f.write( timestamp + '\n')
			# f.write(value + '\n')
			# f.close()

			# Decide if buy/sell/do nothing
			i.process(quote)

			time.sleep(1)

	def get_quote(self, symbol):
		# Get information from siliconinvestor.com
		page = urllib.urlopen('http://markets.siliconinvestor.com/siliconinvestor/quote?Symbol=' + symbol)

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


	def process(i, quote):
		# IF THE STOCK IS DOING BAD LONG-RUN LEAVE IT ALONE
		# if (month_performance < 0):
		#	return
		# message = "NO ACTION"

		# BUY WHEN LOW
		if (quote[VALUE] < quote[DAY_LOW]):
		# DEBUG OFF if (i.toggle == 0):
			# message = "BOUGHT"
			i.buy(quote)
			# DEBUG OFF i.toggle = 1
			return 

		# SELL WHEN HIGH
		if (quote[VALUE] > quote[DAY_HIGH]):
		# DEBUG OFF if (i.toggle == 1):
			#message = "SOLD"
			i.sell(quote)
			# DEBUG OFF i.toggle = 0
			return

		# print message

	def buy(i, quote):
		# What is $1,000 of shares?
		shares = 1000 / quote[VALUE]
		print "shares to buy: " + str(shares)

		# open my_SYMBOL
		f = open('my_' + i.symbol, 'r')
		#print "existing shares: " + f.readlines()[0][:]
		existing_shares = float(f.readlines()[0])
		f.close()

		# add X shares		
		f = open('my_' + i.symbol, 'w')
		existing_shares = existing_shares + shares
		f.write(str(round(existing_shares,2)))
		f.close()

		# open bank
		# TODO: add file locks
		# with FileLock('bank'):
		if True:
			f = open('bank', 'r')
			# take out $1000 for X shares	
			new_balance = float(f.readlines()[0]) - 1000
			f.close()

			f = open('bank', 'w')
			f.write(str(round(new_balance,2)))
			f.close()

		print 'Bought ' + i.symbol + '. ' + str(shares) + ' shares.'

		# wait 5 minutes before doing another trade
		time.sleep(5) 

	def sell(i, quote):
		# open my_SYMBOL
		f = open('my_' + i.symbol, 'r')

		# How many shares do we have?		
		existing_shares = float(f.readlines()[0])
		# If we have no shares to sell, stop
		if (existing_shares == 0):
			f.close()
			return

		# Otherwise, sell
		f.close()
		f = open('my_' + i.symbol, 'w')
		f.write('0')
		f.close()

		# open bank
		# TODO add filelocks
		# with FileLock("bank"):
		if True:
			f = open('bank', 'r')
			# add value gained for X shares		
			new_balance = float(f.readlines()[0]) + (existing_shares * quote[VALUE])
			f.close()
			f = open('bank', 'w')
			f.write(str(round(new_balance,2)))
			f.close()

		print 'Sold ' + i.symbol + '. New balance: ' + str(new_balance)
		# wait 5 minutes before doing another trade
		time.sleep(5)

s = Stockocado()

## Should the mather-s be in a different file? a: no i hate python