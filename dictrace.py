# -*- coding: utf-8 -*-
"""
Created on Fri Nov  4 23:32:56 2022

@author: lcuev
"""
import numpy as np
from string import ascii_lowercase as alphabet
import time
from math import exp,log,cos,sin
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from tqdm import tqdm
np.random.seed(int(time.time()))
alpha = alphabet  + ' '
length = len(alpha)
aspan = range(length)



resol = 100
resolm = resol - 1
rspan = range(resol)

class GetOutOfLoop( Exception ):
    pass

dicts = {}
revdicts = {}

for index,letter in enumerate(alpha):
    dicts[letter] = index
    
for index,letter in enumerate(alpha):
    revdicts[index] = letter

alpha_freqs = np.load('alphabet_wiki.npy',allow_pickle = 'True').item()

def normalize(xyz):
    span = range(len(xyz))
    norm = 0
    ret = []
    for s in span:
        norm += xyz[s] ** 2
    norm = norm ** 0.5
    for s in span:
        ret += [xyz[s] / norm]
    return ret

def coord_to_letters(xyz):
    ret = '0'
    x = xyz[0]
    y = xyz[1]
    z = xyz[2]
    if z > 0:
        x = int(round(x,0)) 
        y = int(round(y,0))
        z = int(round(z,0))
        if x in range(27) and y in range(27) and z in range(27):
            ret = alpha[x] + alpha[y] + alpha[z]
    return ret
    
thresh = 5e-3
def hit_letter(abc):
    ret = 0
    if abc in alpha_freqs:
        freq = alpha_freqs[abc]
        if freq > thresh:
            ret = freq
    return ret

def get_rays(xyz,direc,focal):
    a = 0
    ray_poss = [[[0,0,0] for i in rspan] for j in rspan]
    ray_dirs = [[[0,0,0] for i in rspan] for j in rspan]
    
    
    for i in rspan:
        for j in rspan:
            xp = i / resolm -0.5
            
            yp = j / resolm  - 0.5
            zp = 0
            
            ap = xp / focal
            bp = yp / focal
            cp = focal
            
            al = cos(a) * ap + sin(a) * cp
            bl = bp
            cl = -sin(a) * ap + cos(a) * cp
            
            
            xl = cos(a) * xp + sin(a) * zp + xyz[0] 
            yl = yp + xyz[1]
            zl = -sin(a) * xp + cos(a) * zp + xyz[2]
            xyz2 = [xl,yl,zl]
            
            abc = normalize([al,bl,cl])
            
            ray_poss[i][j] = xyz2
            ray_dirs[i][j] = abc
            
            
    return ray_poss, ray_dirs

def ray_trace(pray,dray):
    speed= 0.5
    ret = []
    for i,r in enumerate(pray):
        ret += [dray[i] * speed + r]
    return ret

def dist(xyz):
    ret = 0 
    for x in xyz:
        ret += x ** 2
    return ret
    

xyz = [13.5,13.5,-10]
direc = [0,0,0]
focal = 2

prays,drays = get_rays(xyz,direc,focal)
scores = [[0 for i in rspan] for j in rspan]
times = [[0 for i in rspan] for j in rspan]


for i in tqdm(rspan):
    for j in rspan:
        letters = '0'
        
        while letters == '0'  and prays[i][j][2] <= 27:
            
            prays[i][j] = ray_trace(prays[i][j], drays[i][j])
            letters = coord_to_letters(prays[i][j])
            hit = hit_letter(letters)
            if hit == 0:
                letters = '0'

        if prays[i][j][2] > 27:
            if sin(prays[i][j][0]*10) > sin(prays[i][j][1]*10):
                hit = 10

        
        scores[i][j] = hit



plt.imshow(scores,cmap = 'Accent')
            
            
        





















