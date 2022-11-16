# -*- coding: utf-8 -*-
"""
Created on Wed Nov  2 21:11:13 2022

@author: lcuev
"""

import requests 
import numpy as np
from bs4 import BeautifulSoup 
from string import ascii_lowercase as alphabet
alpha = alphabet  + ' '
length = len(alpha)
find_forks = False

final_string = ' '
page = requests.get('https://en.wikipedia.org/wiki/Jack_and_Jill')
soup = BeautifulSoup(page.content, 'html.parser')
peas = soup.find_all('p')

for p in peas:
    text = p.get_text()
    for lett in text:
        a = lett.lower()
        if a in alpha:
            final_string += a

    final_string += ' '

if find_forks:
    forks = soup.find_all('a')
    wikis = []
    for f in forks:
        if f.has_attr('href'):
            possible = f['href']
            if possible[:6] == '/wiki/' and ':' not in possible and possible not in wikis:
                wikis += [possible]
                
                
    
    for wiki in wikis:
        link = 'https://en.wikipedia.org' + wiki
        page = requests.get(link)
        soup = BeautifulSoup(page.content, 'html.parser')
        peas = soup.find_all('p')
    
        for p in peas:
            text = p.get_text()
            for lett in text:
                a = lett.lower()
                if a in alpha:
                    final_string += a
            final_string += ' '


freqs = {} 
for a in alpha:
    for b in alpha:
        for c in alpha:
            key = a + b + c
            freqs[key] = 0

text = final_string

print(final_string)

for index in range(1,len(text)-1):
    if text[index] in alpha and text[index - 1] in alpha and text[index + 1] in alpha:
        key = text[index-1] + text[index] + text[index + 1]
        if text[index - 1] == ' ' and text[index + 1] == ' ':
            if text[index] == 'a':# or text[index] == 'i':
                freqs[key] += 1
        else:
            freqs[key] += 1
norm = 0
for a in alpha:
    for b in alpha:
        for c in alpha:
            key = a + b + c
            norm += freqs[key]
            
smoother = 0.01
t = 0
for a in alpha:
    for b in alpha:
        for c in alpha:
            key = a + b + c
            freqs[key] = (freqs[key] + smoother)/(norm + smoother * t)
            t += 1
            
            
            



with open('3letter_wiki.csv', 'w') as f:
    [f.write('{0},{1}\n'.format(key, value)) for key, value in freqs.items()]

np.save('alphabet_wiki.npy',freqs)



            
    