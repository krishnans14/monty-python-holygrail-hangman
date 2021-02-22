"""
This file shows how to scrap the montypython.net page to get some popular monty python holy grail quotes.
In this approach, we restrict only to those quotes for which the site admin has uploaded a corresponding .wav file.
This way, we have a restricted number of quotes (179 in this case)
"""
import bs4
from bs4 import BeautifulSoup
import requests
import re
import pickle

import sys
sys.setrecursionlimit(10000) #to avoid issues related to max recursion depth reached


# Sources - Holy grail
sources = [requests.get('https://montypython.net/grailmm1.php').text,
           requests.get('https://montypython.net/grailmm2.php').text,
           requests.get('https://montypython.net/grailmm3.php').text]

# Finding all the unique quotes for which there were audio clips
monty_python_quotes = []
quote = None
for source in sources:
    soup = BeautifulSoup(source, 'lxml')
    for aa in soup.find_all('a'):
        if 'href' in aa.attrs: #looking for only those which are hyperlinks
            if '.wav' in  aa.attrs['href']: # We are only looking for those quotes which have an associated sound file
                if len(aa.contents) > 1:
                    quote = aa.contents[0]
                else:
                     quote = aa.contents

        if quote is None:
            pass
        else:
             if isinstance(quote, list):
                    if isinstance(quote[0], bs4.element.NavigableString): # It was observed that all the valid quotes were of this type
                        if len(quote[0].split(' ')) > 1 : # To avoid single word quotes that were mostly useless.
                            monty_python_quotes.append(quote[0])

monty_python_quotes = list(dict.fromkeys(monty_python_quotes))

with open('mp_quotes.file', "wb") as f:
    pickle.dump(monty_python_quotes, f, protocol=pickle.HIGHEST_PROTOCOL)
