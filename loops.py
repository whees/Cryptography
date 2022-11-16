# -*- coding: utf-8 -*-
"""
Created on Mon Nov  7 02:12:57 2022

@author: lcuev
"""
import matplotlib.pyplot as plt
import numpy as np
from string import ascii_lowercase as alphabet
from math import cos,sin



alpha = alphabet  
length = len(alpha)
length_ = length - 1


def get_rand_cipher():
    ordr = np.random.choice(26,26,replace = False)
    ret = {}
    for index,letter in enumerate(alphabet):
        ret[letter] = alphabet[ordr[index]]
    return ret

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
            
def norm(a,b):
    return a / (a**2 + b**2) ** 0.5,b / (a**2 + b**2) ** 0.5


            


n_sims = 10000
sims = range(n_sims)
freqs = [0 for i in range(length)]
tots = 0

for sim in sims:
    cipher = get_rand_cipher()
    loops = get_loops(cipher)
    lens = []
    for loop in loops:
        lens += [len(loop)]
    freqs[max(lens) - 1] += 1
    tots += 1
       
cum_sums = []
sm = 0
for freq in freqs:
    freq /= tots
    sm += freq
    cum_sums += [sm]

plt.bar(range(1,length+1),freqs)
plt.show()
plt.bar(range(1,length+1),cum_sums,color = "Blue")
plt.xlabel("Max Loop Length")
plt.ylabel("Cumulative Frequency")
plt.show()



letter_angle = {}
for i,a in enumerate(alpha):
    letter_angle[a] = i / (length) * 2 * 3.14
    


resol = 1000
image = [[0 for i in range(resol)] for k in range(resol)]


for i in range(resol):
    for j in range(resol):
        if (i - resol / 2)**2 + (j-resol/2)**2 > 300**2 -2000 and (i - resol / 2)**2 + (j-resol/2)**2 < 300**2 + 2000:
            image[i][j] = 1


   
cipher = get_rand_cipher()
loops = get_loops(cipher)    
speed = 0.01
r = 300

for c,loop in enumerate(loops):
    for i,letter in enumerate(loop):
        if i < len(loop) - 1:
            if letter != loop[i + 1]:
                a1 = letter_angle[letter] 
                x1 = r * sin(a1) + resol / 2 
                y1 = r * cos(a1) + resol / 2 
                xpos = x1
                ypos = y1
                image[int(xpos)][int(ypos)] = c + 2
                a2 = letter_angle[loop[i+1]] 
                x2 = r * sin(a2) + resol / 2 
                y2 = r * cos(a2) + resol / 2 
                dirx, diry = norm(x2-x1,y2-y1)
                t = 0
                while (xpos - resol / 2) ** 2 + (ypos - resol / 2) ** 2 < 300 ** 2 or t < 3:
                    xpos += dirx * speed
                    ypos += diry * speed
                    for z in range(9):
                        image[int(xpos) + z - 4][int(ypos) + z - 4] = c + 2
                    t += 1

plt.imshow(image,interpolation = 'gaussian',cmap = 'gnuplot2')
for a,i in enumerate(alpha):
    angle = a / length * 2 * 3.14 - 0.1
    r = 350
    x = r * sin(angle) + resol / 2 - 15
    y = r * cos(angle) + resol / 2 + 10
    plt.text(x,y,i,color='white')
    letter_angle[i] = angle
    


