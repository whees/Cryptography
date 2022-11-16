# -*- coding: utf-8 -*-
"""
Created on Sun Nov  6 01:48:58 2022

@author: lcuev
"""
import csv
import matplotlib.pyplot as plt
ran = range(19)
avegs = [[0 for i in ran]  for j in ran]
varss = [[0 for i in ran] for j in ran]

  
# Open file 
with open('rework6_averages.csv') as file_obj:
      
    # Create reader object by passing the file 
    # object to reader method
    reader_obj = csv.reader(file_obj)
      
    # Iterate over each row in the csv 
    # file using reader object
    for row in reader_obj:
        if row != []:
            avegs[int(row[0])][int(row[1])]= float(row[2])
            
with open('rework6_variances.csv') as file_obj:
      
    # Create reader object by passing the file 
    # object to reader method
    reader_obj = csv.reader(file_obj)
      
    # Iterate over each row in the csv 
    # file using reader object
    for row in reader_obj:
        if row != []:
            varss[int(row[0])][int(row[1])]= float(row[2])
            
"""
vflat1 = []
aflat1 = []
vflat2 = []
aflat2 = []
vflat3 = []
aflat3 = []


r1 = []
r2 = []
r3 = []
rats = [1/4,1/3,1/2,1,2,3,4]

for i in ran:
    for j in ran:
        if rats[i] > rats[j]:
            aflat1 += [avegs[i][j]]
            vflat1 += [varss[i][j]]
            r1 += [rats[i] * rats[j]]
        elif rats[i] == rats[j]:
            aflat2 += [avegs[i][j]]
            vflat2 += [varss[i][j]]
            r2 += [rats[i] * rats[j]]
        else:
            aflat3 += [avegs[i][j]]
            vflat3 += [varss[i][j]]
            r3 += [rats[i] * rats[j]]
"""

plt.imshow(avegs,cmap = "Greens",origin = 'lower')
plt.colorbar()
plt.show()
plt.imshow(varss, cmap = "Blues",origin = 'lower')
plt.colorbar()

"""
plt.xlabel('Unseeded Rate')
plt.ylabel('Mean')
plt.xscale('log')
plt.title('Mean vs. Unseeded Rate')
plt.scatter(rats,avegs,color = 'Green')
plt.show()
plt.xlabel('Solo Rate')
plt.ylabel('Variance')
plt.xscale('log')
plt.title('Variance vs. Unseeded Rate')
plt.scatter(rats,varss,color = 'Blue')
"""

