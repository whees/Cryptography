# -*- coding: utf-8 -*-
"""
Created on Thu Oct 27 15:51:34 2022

@author: lcuev
"""
import numpy as np
from string import ascii_lowercase as alphabet
import matplotlib.pyplot as plt

data = np.load('wp.npz')
text = str(data['text'])


alpha = alphabet  + ' '
length = len(alpha)

freqs = {} 
for a in alpha:
    for b in alpha:
        for c in alpha:
            key = a + b + c
            freqs[key] = 0
dicts = {}
revdicts = {}

field_names = ['combination','frequency']

for index,letter in enumerate(alpha):
    dicts[letter] = index
    
for index,letter in enumerate(alpha):
    revdicts[index] = letter


for index in range(1,len(text)-1):
    if text[index] in dicts and text[index - 1] in dicts and text[index + 1] in dicts:
        if text[index - 1] == ' ' and text[index + 1] == ' ':
            if text[index] == 'a':# or text[index] == 'i':
                key = text[index-1] + text[index] + text[index + 1]
                freqs[key] += 1
        else:
            key = text[index-1] + text[index] + text[index + 1]
            freqs[key] += 1
norm = 0
for a in alpha:
    for b in alpha:
        for c in alpha:
            key = a + b + c
            norm += freqs[key]
            
smoother = 1
t = 0
for a in alpha:
    for b in alpha:
        for c in alpha:
            key = a + b + c
            freqs[key] = (freqs[key] + smoother)/(norm + smoother * t)
            t += 1
            
            
            



with open('3letter_data.csv', 'w') as f:
    [f.write('{0},{1}\n'.format(key, value)) for key, value in freqs.items()]
    
np.save('alphabet_frequencies.npy',freqs)


            
    

        

