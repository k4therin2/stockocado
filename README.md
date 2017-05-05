# Stockocado

Pet project to __(a)__ get better at python and __(b)__ get better at statistics and __(c)__ maybe machine learning at some point?

Reads current quotes on different stocks from the NASDAQ, and decides when to buy/sell.

## How it works

`Stockocado.py` reads from a list of stock symbols (`symbols.txt`) and creates a new thread for each company. Each thread then periodically checks the stock price, and decides if it should sell/buy at that moment.

When the stock price goes __below__ the day's current range, Stockocado buys __$1,000__ worth of shares.

When the stock price goes __above__ the day's current range, Stockocado sells __all__ of its existing shares. 

Stockocado starts with $10,000,000 in the bank.

## Current issues:
 1. ~~File reading/writing - Was getting "index out of bounds" errors when opening files with mode r+ (read and overwrite), so currently am doing excessive file opening/closing specifically defining modes "r" and "w"~~ Fix: _filename.seek()_ after read/writes to reset cursor!

## To do:

* Like... don't keep track of shares by creating a new file for each company
* Ditto for the "bank"
* Then write a more mature buy/sell algorithm! :-D _...ah, the naivite of youth..._

# Python things learned:
  * ~ * context managers * ~ makes things like file access a heck of a lot easier
  * scripting in python with #!s
  * class-object inheritance (python 2.1+)
  * `requirements.txt` files should be included
  * the `print()` function (when combined w string formatters) makes printing... a heck of a lot easier
  * "magic" functions (sepcifically \__init\__ in this case, to prevent code from being run when it isn't meant to be)
  * descriptors (unused) are A Thing that seem like they'll be useful at some point
  
Shoutout to [Andrew](https://github.com/ajm188) for giving me python guidance.
