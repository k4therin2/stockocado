import threading
from bs4 import BeautifulSoup
import urllib
import time
from time import sleep, gmtime, strftime
from filelock import FileLock

class Stockocado():
	global VALUE, TIME, DAY_LOW, DAY_HIGH, SYMBOL, lock, toggle
	VALUE = 0
	TIME = 1
	DAY_LOW = 2
	DAY_HIGH = 3
	SYMBOL = 4
	toggle = 0
	lock = threading.Lock()

	def read_symbols(self):
		symbol_array = [line.rstrip('\n') for line in open('v_symbols.txt')]
		return symbol_array

	def __init__(self):
		# Get symbols of stocks to watch (CRM, NTFX, GOOG, etc.)
		symbols = self.read_symbols()

		# put some dolla dolla in that pocket
		f = open('bank', 'w')
		f.write('10000000')
		f.close()
		#self.lock = threading.Lock()

		# each symbol gets their own thread
		for symbol in range(len(symbols)):	
			threading.Thread(target=self._listener, args=(symbols[symbol],)).start()

	def _listener(i, symbol):
		# get thread id 

		# DEBUG OFF i.toggle = 0
		print 'listener started on: ' + symbol	

		# Keep track of how many shares you have	
		f = open('my_' + symbol, 'w')
		f.write('0')
		f.close()

		while(True):
			# Get information (value, timestamp, monthly performance, current day high, current day low)
			quote = i.get_quote(symbol)			

			if (len(quote) < 3):
				# Failure if parsing issue with layout 
				if (quote[0] == "FAILURE"):
					print quote[1]
					return
				# Wait a bit if connection error, then try again
				if (quote[0] == "IOError"):
					print quote[1]
					time.sleep(5)
			else:
				# Print to console
				# value = quote[VALUE]
				# value = str(round(value,2))
				# timestamp = quote[TIME]
				# print '[ ' + symbol + ' ] ' + value

				# Save information
				# f = open(symbol, 'a')
				# f.write( timestamp + '\n')
				# f.write(value + '\n')
				# f.close()

				# Decide if buy/sell/do nothing
				i.process(quote)

				# sleep(1)

	def get_quote(i, symbol):
		# Get information from siliconinvestor.com
		try:
			page = urllib.urlopen('http://markets.siliconinvestor.com/siliconinvestor/quote?Symbol=' + symbol)
			timestamp = strftime("%Y-%m-%d %H:%M:%S", gmtime())
			soup = BeautifulSoup(page, "html.parser")
		except IOError:
			return ["IOError", "Name Resolution Down for [" + symbol + "]."]

		# GET SHARE VALUE
		value_div = soup.find(id='quotenav1_field_price')

		try:
			value = float(value_div.contents[0][:])
		except ValueError: 
			# TEMINATE IF PAGE LAYOUT IS WEIRD
			return ["FAILURE", 'Terminating [' + symbol + '].' ]

		# GET RANGE
		day_range = str(soup.findAll('tr', attrs={'class':'row_range'}))
		day_range = day_range[81:]
		day_range = day_range.split('<')
		day_range = day_range[0].split('-')

		# IF EMPTY, QUIT THREAD, PAGE LAYOUT WEIRD 
		if (len(day_range[0]) < 1):
			return ["FAILURE", 'Terminating [' + symbol + '].' ]

		# GET LOW FOR DAY
		day_low = float(day_range[0])
		# GET HIGH FOR DAY
		day_high = float(day_range[1])

		return value, timestamp, day_low, day_high, symbol


	def process(i, quote):
		# print 'Processing [' + quote[SYMBOL] + ']: V L H ' + str(quote[VALUE]) + ' ' + str(quote[DAY_LOW]) + ' ' + str(quote[DAY_HIGH]) 
		
		# BUY WHEN LOW
		if (quote[VALUE] == quote[DAY_LOW]):
		# DEBUG OFF if (i.toggle == 0):
			# message = "BOUGHT"
			i.buy(quote)
			# DEBUG OFF i.toggle = 1
			return 

		# SELL WHEN HIGH
		if (quote[VALUE] == quote[DAY_HIGH]):
		# DEBUG OFF if (i.toggle == 1):
			# message = "SOLD"
			i.sell(quote)
			# DEBUG OFF i.toggle = 0
			return

		# print message

	def buy(i, quote):
		# What is $1,000 of shares?
		shares = 1000 / quote[VALUE]
		# print "shares to buy: " + str(shares)

		# open my_SYMBOL
		f = open('my_' + quote[SYMBOL], 'r')
		#print "existing shares: " + f.readlines()[0][:]
		existing_shares = float(f.readlines()[0])
		f.close()

		# add X shares		
		f = open('my_' + quote[SYMBOL], 'w')
		existing_shares = existing_shares + shares
		f.write(str(round(existing_shares,2)))
		f.close()

		# open bank
		# TODO: add file locks
		# with FileLock('bank'):
		if True:
			lock.acquire()
			f = open('bank', 'r')
			# take out $1000 for X shares	
			new_balance = float(f.readlines()[0]) - 1000
			f.close()

			f = open('bank', 'w')
			f.write(str(round(new_balance,2)))
			f.close()
			lock.release()

		print 'Bought [' + quote[SYMBOL] + ']. ' + str(shares) + ' shares. New balance: ' + str(round(new_balance,2))

		# wait before doing another trade
		sleep(30) 

	def sell(i, quote):
		# open my_SYMBOL
		f = open('my_' + quote[SYMBOL], 'r')

		# How many shares do we have?		
		existing_shares = float(f.readlines()[0])
		# If we have no shares to sell, stop
		if (existing_shares == 0):
			print 'Tried to sell [' + quote[SYMBOL] +'] but we have no shares yet.'
			f.close()
			return

		# Otherwise, sell
		f.close()
		f = open('my_' + quote[SYMBOL], 'w')
		f.write('0')
		f.close()

		# open bank
		# TODO add filelocks
		# with FileLock("bank"):
		if True:
			lock.acquire()
			f = open('bank', 'r')
			# add value gained for X shares		
			new_balance = float(f.readlines()[0]) + (existing_shares * quote[VALUE])
			f.close()
			f = open('bank', 'w')
			f.write(str(round(new_balance,2)))
			f.close()
			lock.release()

		print '==> SOLD ==> ' + quote[SYMBOL] + '. New balance: ' + str(new_balance)
		# wait before doing another trade
		# sleep(5)

s = Stockocado()