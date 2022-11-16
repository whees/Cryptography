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
from csv import writer


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

_last_print_len = 0 
def reprint(msg, finish=False): 
    global _last_print_len 
     
    print(' '*_last_print_len, end='\r') 
     
    if finish: 
        end = '\n' 
        _last_print_len = 0 
    else: 
        end = '\r' 
        _last_print_len = len(msg) 
     
    print(msg, end=end) 
            
def resum(log_dict):
    ret = 0
    for key in log_dict:
        ret += exp(log_dict[key])
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

    

def get_rand_cipher():
    ordr = np.random.choice(26,26,replace = False)
    ret = {}
    for index,letter in enumerate(alphabet):
        ret[letter] = alphabet[ordr[index]]
    ret[' '] = ' '
    return ret

def should_swap(proposed_score, current_score,rate):
    diff = rate / abs(rate) * (proposed_score - current_score)
    if diff > 0:
        comp = 1.1
    else:
        comp = exp(diff*abs(rate))
    
    return comp > np.random.random()


def should_swap_v2(proposed_score, current_score,rate):
    #diff = proposed_score - current_score
    diff =  proposed_score - current_score
    ret = False
    if diff > 0 or exp(diff) > np.random.random():
        ret = True
    
    return ret

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





    
primary_rates = [-1/4]
secondary_rates = [1/4]


cipher = get_rand_cipher() 
unscrambled = ' jack and jill went up the hill to fetch a pail of water '
scrambled = apply_cipher(cipher,unscrambled)
n_sims = 30
sims = range(n_sims)
averages = [[0 for r in primary_rates] for s in secondary_rates]
varis = [[0 for r in primary_rates] for s in secondary_rates]

averages2 = [[0 for r in primary_rates] for s in secondary_rates]
varis2 = [[0 for r in primary_rates] for s in secondary_rates]


print('\n')
print('encrypted phrase: ', scrambled)
print('\n') 

for i,prime_rate in enumerate(tqdm(primary_rates)):
    for j,sec_rate in enumerate(tqdm(secondary_rates)):
        best_scos = []
        best_phrases = []
        all_phrases = []
        for sim in sims:
            max_swaps = 3000
            decipher = get_rand_cipher()
            max_futures = 7
            present_futures = 0
            futures = []
            phrases = [] 
            
            deciphered = apply_cipher(decipher, scrambled)
            #phrase_freqs = get_freq_dict(deciphered)
            best_score = get_score(deciphered)
            times = []
            bests = []
            rate = prime_rate
            

            
            for swap in range(max_swaps):
                proposed_decipher = propose_decipher(decipher)
                phrase = apply_cipher(proposed_decipher,scrambled)
                #phrase_freqs = get_freq_dict(phrase)
                temp_score = get_score(phrase)
                do_swap = should_swap(temp_score, best_score,rate)
                if do_swap:
                    if temp_score > best_score:
                        best_acc = get_score(phrase)
                    if temp_score > best_score and present_futures < max_futures and swap > max_swaps/2:
                        futures += [decipher]
                        present_futures= len(futures)
                    decipher = proposed_decipher
                    best_score = temp_score
                    bests += [best_score]
                    times += [swap]
                    
            
            print(present_futures)
 
  
            phrases += [phrase]
           
            best_phrase = phrase
            rate = sec_rate
            
            best_seeds = [0 for i in futures]
                
     
            
            
            for n,future in enumerate(futures):
                t = [0]
                decipher = future
                deciphered = apply_cipher(decipher,scrambled)
                #phrase_freqs = get_freq_dict(deciphered)
                best_score = get_score(deciphered)
                best_best = best_score
                rate = sec_rate
            
            
                for swap in range(max_swaps):
                    proposed_decipher = propose_decipher(decipher)
                    phrase = apply_cipher(proposed_decipher,scrambled)
                    #phrase_freqs = get_freq_dict(phrase)
                    temp_score = get_score(phrase)
                    do_swap = should_swap(temp_score, best_score,rate)
                    if do_swap:
                        decipher = proposed_decipher
                        best_score = temp_score
                        if best_score > best_best:
                            best_best = best_score
                            best_phrase = phrase
                            best_seeds[n] = best_score
                        
                phrases += [phrase]
                
            accuracies2 = []
            for phs in phrases:
                ph_acc = get_score(phs)
                accuracies2 += [ph_acc]  
            initial = accuracies2[0]
            after = max(best_seeds) 
            plt.scatter(best_acc,after)
            best_scos += [after]
            all_phrases += phrases
            best_phrases += [best_phrase]
        plt.title(f'{round(prime_rate,2)}, {round(sec_rate,2)} seeding run vs. seeds')
        plt.xlabel('seeding run best accuracy')
        plt.ylabel('best seed accuracy')
        plt.show()
        accuracies = []
        for phs in best_phrases:
            ph_acc = get_score(phs)
            accuracies += [ph_acc]
        accuracies2 = []
        
        
        varis[i][j] = np.var(accuracies)
        averages[i][j] = np.average(accuracies)
        avg = np.average(best_scos)
        print('\n',avg)

        
    
        accuracies2 = []
        for phs in all_phrases:
            ph_acc = get_score(phs)
            accuracies2 += [ph_acc]
        
        varis2[i][j] = np.var(accuracies2)
        averages2[i][j] = np.average(accuracies2)
        
        
        
        with open('playmean.csv', 'a') as f:
            [f.write('{0},{1},{2}\n'.format(i, j,averages[i][j]))]
            
        with open('playvar.csv', 'a') as f:
            [f.write('{0},{1},{2}\n'.format(i, j,varis[i][j]))]
            

            
        
        








    
