from bs4 import BeautifulSoup
import urllib

symbol = 'NFLX'

print "Give a NASDAQ symbol:"
symbol = raw_input()

page = urllib.urlopen('http://nasdaq.com/symbol/' + symbol)
soup = BeautifulSoup(page, "html.parser")
quote_div = soup.find(id='qwidget_lastsale')
quote = float(quote_div.contents[0][1:])

print quote