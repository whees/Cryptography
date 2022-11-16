# -*- coding: utf-8 -*-
"""
Created on Sat Nov 12 16:47:29 2022

@author: lcuev
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Oct 27 15:50:40 2022

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
    
init_ciph = {}
for letter in alpha:
    init_ciph[letter] = letter



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
    if rate != 0:
        diff = rate/abs(rate)*(proposed_score - current_score)
    else:
        diff = 0
    if diff > 0:
        comp = 1.1
    else:
        comp = exp(diff*abs(rate))
    
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

n_pics = 1
pics = range(n_pics)

cipher = get_rand_cipher() 
unscrambled = ' jack and jill went up the hill to fetch a pail of water '
scrambled = apply_cipher(cipher,unscrambled)
for pic in pics:
    primary_rates = np.arange(-0.5,1,0.01)
    rates = []
    sets = []
    loops = []
    scores = []
    alphs = []
    n_loops = []
    
    for rate in tqdm(primary_rates):
        primary_rate = rate
        secondary_rate = primary_rate
        
        
        
        
    
        n_sims = 1
        future_decipher = ''
        max_swaps = 3000
        best_best = 0
        
        for sim in range(n_sims):
            decipher = init_ciph
            deciphered = apply_cipher(decipher, scrambled)
            best_score = get_score(deciphered)
            if sim == 0:
                best_best = best_score
            rate = primary_rate
            phrase = ''
            
            
            for swap in range(max_swaps):
                proposed_decipher = propose_decipher(decipher)
                phrase = apply_cipher(proposed_decipher,scrambled)
                temp_score = get_score(phrase)
                do_swap = should_swap(temp_score, best_score,rate)
                if do_swap:
                    decipher = proposed_decipher
                    best_score = temp_score
                    if rate > 0:
                        if best_score > best_best:
                            best_best = best_score
                            future_decipher = decipher
                    elif rate < 0:
                        if best_score < best_best:
                            best_best = best_score
                            future_decipher = decipher
                    else:
                        future_decipher = decipher
            
        phrase_dict = {}                   
        sec_swaps = 1000
        if future_decipher == '':
            future_decipher = decipher
      
                    
                    
        for swap in range(sec_swaps):
            proposed_decipher = propose_decipher(future_decipher)
            phrase = apply_cipher(proposed_decipher,scrambled)
            temp_score = get_score(phrase)
            do_swap = should_swap(temp_score, best_score,rate)
            if do_swap:
                decipher = proposed_decipher
                best_score = temp_score
                if phrase in phrase_dict:
                    phrase_dict[phrase] += 1
                else:
                    phrase_dict[phrase] = 1
        
       
        
        
        
        total = 0
        for phrase in phrase_dict:
            total += phrase_dict[phrase]
        
        for phrase in phrase_dict:
            phrase_dict[phrase] /= total
            
        order_phrases = sorted(phrase_dict.items(),key = lambda x:x[1],reverse = True)
        
        score_phrases = {}
        for order in order_phrases:
            score_phrases[str(order[0])] = get_score(str(order[0]))
        
        
        for order in order_phrases:
            score = score_phrases[str(order[0])]
            if order[1] > 0/50:
                plt.scatter(rate,score,alpha = order[1])
    
            
            rates += [rate]
            sets += [score]
            alphs += [order[1]]
 
                
            
    
    
    plt.title('annealing rate vs. score')
    plt.xlabel('annealing rate')
    plt.ylabel('score')
    #plt.axhline(-348.841, c = 'black',linestyle = '--')
    fname = 'Anim2/Frame' + str(pic) + str(int(time.time())) + '.png'
    plt.savefig(fname)
    plt.clf()
    
  





    
