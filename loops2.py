# -*- coding: utf-8 -*-
"""
Created on Sat Nov 12 16:47:29 2022

@author: lcuev
"""
import numpy as np
from string import ascii_lowercase as alphabet
import time
from math import exp,log
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from tqdm import tqdm


np.random.seed(int(time.time()))
alpha = alphabet  + ' '
length = len(alpha)

dicts = {}
revdicts = {}

for index,letter in enumerate(alpha):
    dicts[letter] = index
    
for index,letter in enumerate(alpha):
    revdicts[index] = letter
    




alpha_freqs = np.load('alphabet_wiki.npy',allow_pickle = 'True').item()

def get_freq_dict(string):
    ret = {}
    for a in alpha:
        for b in alpha:
            for c in alpha:
                key = a + b + c
                ret[key] = 0
    for i in range(1,len(string) - 1):
        key = string[i-1] + string[i] + string[i+1]
        if key in ret:
            ret[key] +=1
    
    norm = 0
    for a in alpha:
        for b in alpha:
            for c in alpha:
                key = a + b + c
                norm += ret[key]
    for a in alpha:
        for b in alpha:
            for c in alpha:
                key = a + b + c
                ret[key] /= norm     
    return ret

#alpha_freqs = get_freq_dict(' jack and jill went up the hill to fetch a pail of water ')

def freq_score(ph):
    ret = {}
    for i in range(1,len(ph)-1):
        key = ph[i-1] + ph[i] +  ph[i + 1]
        if key in alpha_freqs:
            if key in ret:
                ret[key] += log(alpha_freqs[key]) 
            else:
                ret[key] = log(alpha_freqs[key])
    return ret


def get_score(ph):
    ret = 0
    for i in range(1,len(ph)-1):
        if ph[i-1] in alpha and ph[i] in alpha and ph[i+1] in alpha:
            key = ph[i-1] + ph[i] + ph[i + 1]
            k = alpha_freqs[key]
            if  k > 0:
                ret += log(k)
            else:
                ret -= 10
    return ret

def apply_cipher(dec,ph):
    ret = ''

    for index,i in enumerate(ph):
        if i in alpha:
            ret += dec[i]
        else:
            ret += ph[index]
    return ret

def propose_decipher(ciph):
    first_letter = np.random.choice(26)
    second_letter = np.random.choice(26)

    while(first_letter == second_letter):
        second_letter = np.random.choice(26)

    new_cipher = {}
    for letter in alphabet:
        if (letter == alphabet[first_letter]):
            new_cipher[letter] = ciph[alphabet[second_letter]]
        elif (letter == alphabet[second_letter]):
            new_cipher[letter] = ciph[alphabet[first_letter]]
        else:
            new_cipher[letter] = ciph[letter]
    new_cipher[' '] = ' '
    return new_cipher
def get_loops(ciph):
    loops = []
    n_loops = 0
    repeats = ''
    for key in ciph:
        if key not in repeats:
            loops += [key]
            cont = ciph[key]
            while cont != key:
                repeats += cont
                loops[n_loops] += cont
                cont = ciph[cont]
            n_loops += 1
    return loops
    

def get_rand_cipher():
    ordr = np.random.choice(26,26,replace = False)
    ret = {}
    for index,letter in enumerate(alphabet):
        ret[letter] = alphabet[ordr[index]]
    ret[' '] = ' '
    return ret

def should_swap(proposed_score, current_score,rate):
    diff = proposed_score - current_score
    if diff > 0:
        comp = 1.1
    else:
        comp = exp(diff*rate)
    
    return comp > np.random.random()


def accuracy(phrase1,phrase2):
    ret = 0
    if len(phrase1) == len(phrase2):
        tot = 0
        for index,letter in enumerate(phrase1):
            if letter != ' ':
                if letter == phrase2[index]:
                    ret += 1
                tot += 1
                
                    
                
        ret /= tot
    return ret

tests = [1,2,3,4,5]
test_bins = [[0 for i in range(26)] for j in tests]
n_c = 0
cipher = {}
while n_c != 13:
    cipher = get_rand_cipher() 
    n_c = len(get_loops(cipher))
unscrambled = ' jack and jill went up the hill to fetch a pail of water '
scrambled = apply_cipher(cipher,unscrambled)



for ind,test in enumerate(tests):
    primary_rates = [1/test for i in range(2000)]
    rates = []
    sets = []
    loops = []
    scores = []
    alphs = []
    n_loops = [0 for i in range(26)]
    
    for rate in tqdm(primary_rates):  
        max_swaps = 3000
        decipher = get_rand_cipher()
        deciphered = apply_cipher(decipher, scrambled)
        best_score = get_score(deciphered)
        phrase = ''
        
        
        for swap in range(max_swaps):
            proposed_decipher = propose_decipher(decipher)
            phrase = apply_cipher(proposed_decipher,scrambled)
            temp_score = get_score(phrase)
            do_swap = should_swap(temp_score, best_score,rate)
            if do_swap:
                decipher = proposed_decipher
                best_score = temp_score
               
            
        loops = get_loops(decipher)
        n = len(loops) - 1
        n_loops[n] += 1
        
    tot  = 0
    for loop in n_loops:
        tot += loop
    
    for n,loop in enumerate(n_loops):
        n_loops[n] /= tot    
    
    test_bins[ind] = n_loops

colors = ['red','lime','blue','magenta','brown']
for ind,tb in enumerate(test_bins):
    plt.plot(range(1,27),tb,marker = 'o',color=colors[ind],label = f'{tests[ind]}^(-1) loop cipher')
    
plt.legend()
plt.xlim(0,15)
plt.ylim(0,0.35)    
plt.title('number of loops vs. frequency of occurence')
plt.xlabel('number of loops')
plt.ylabel('frequency of occurence')
fname = 'Anim2/Frame' + str(int(time.time())) + '.png'
plt.savefig(fname)


  





    
