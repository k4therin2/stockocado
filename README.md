# Stockocado

Reads current quotes on different stocks from the NASDAQ, and decides when to buy/sell.

## How it works

`Stockocado.py` reads from a list of stock symbols (`symbols.txt`) and creates a new thread for each company. Each thread then periodically checks the stock price, and decides if it should sell/buy at that moment.

When the stock price goes __below__ the day's current range, Stockocado buys __$1,000__ worth of shares.

When the stock price goes __above__ the day's current range, Stockocado sells __all__ of its existing shares. 

Stockocado starts with $10,000,000 in the bank.
