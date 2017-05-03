# Stockocado

Reads current quotes on different stocks from the NASDAQ, and decides when to buy/sell.

## How it works

`Stockocado.py` reads from a list of stock symbols (`symbols.txt`) and creates a new thread for each company. Each thread then periodically checks the stock price, and decides if it should sell/buy at that moment.

When the stock price gos below the day's current range, Stockocado buys $1,000 worth of shares.
When the stock price goes above the day's current range, Stockocado sells all of its existing shares. 

Stockocado starts with $10,000,000 in the bank.
