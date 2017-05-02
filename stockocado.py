## TODO

## [x] 1. Price Retriever
## [o] 2. Price Listner
## [ ] 3. Price Grapher
## [ ] 4. Buy/Sell decision
## [o] 5. Thread 1-4 for multiple stocks

import threading
from bs4 import BeautifulSoup
import urllib
import time

class Stockocado():

	def read_indexes(self):
		index_array = [line.rstrip('\n') for line in open('indexes.txt')]
		return index_array

	def __init__(self):
		indexes = self.read_indexes()
		for index in range(len(indexes)):	
			threading.Thread(target=self._listener, args=(indexes[index],)).start()

	def _listener(i, index):
		print 'listener started on: ' + index

		while(True):
			quote = str(round(i.get_quote(index),2))
			print '[ ' + index + ' ] ' + quote
			f = open(index, 'a')
			f.write(quote)
			f.write('\n')
			f.close()
			time.sleep(1)

	def get_quote(self, index):
		page = urllib.urlopen('http://nasdaq.com/symbol/' + index)
		soup = BeautifulSoup(page, "html.parser")
		quote_div = soup.find(id='qwidget_lastsale')
		quote = float(quote_div.contents[0][1:])
		return quote

s = Stockocado()
