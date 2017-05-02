## TODO

## [x] 1. Price Retriever
## [o] 2. Price Listner
## [ ] 3. Price Grapher
## [ ] 4. Buy/Sell decision
## [o] 5. Thread 1-4 for multiple stocks

import threading

class Stockocado():

	def read_indexes(self):
		index_array = [line.rstrip('\n') for line in open('indexes.txt')]
		return index_array

	def __init__(self):
		indexes = self.read_indexes()
		for index in range(len(indexes)):	
			threading.Thread(target=self._listener, args=(indexes[index],)).start()

	def _listener(i, index):
		print 'listener started on:' + index



s = Stockocado()
