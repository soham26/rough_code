# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>


import numpy as np
import csv as csv
import sys
import time
import random
ob= csv.reader(open('C:\\Users\\prashant\\Documents\\Summer_project\\data.csv','rb'))
header=ob.next()
data=[]
for line in ob:
    data.append(line)
    
data=np.array(data)

states=[]

for i in range(1,len(data[0,:])):
    states.append(data[0,i])
    
states,len(states)

nk=5

ini=[]     # ini will be storing the medoid centers during the whole time the program runs, and finally will give the optimum medoids.
import random
#randomly iniatilize the medoid centres
# I have chosen nk=5, as in the no. of clusters we are going to have

def findpos(ini,data):
    index=[]
    for k in range(0,len(ini)):
        for i in range(0,len(data)):
            if ini[k]==data[0,i]:
                index.append(i)
    return index


pos=findpos(ini,data)
dis=[]
#calculate distances of various non-medoid points from the medoid points one by one
for k in range(0,len(ini)):
    print 'The position of the medoid centre',ini[k],'in the dataset csv file is ',pos[k]
    mdis=[] 
    for i in range(1,31):
        if data[i,pos[k]]=='':
            mdis.append(data[pos[k],i])
        else:
            mdis.append(data[i,pos[k]])
    dis.append(mdis)
        



print ':ini: is the array storing the initial medoid cluster centres'
print ':dis: is the array storing the distances of each state from the medoid, which will help in determining the cost function'

# STEP1
# medoid have been initalized || and distances of each cluster point from the cluster medoids have been stored (unnecesary) ||
# STEP 2
# Association of non-medoid points to medoid points , i.e every point chooses the nearest medoid


# function for associating the various nom-medoid points to the medoids, given a current set of medoids as input

def assoc(pos): # takes the position array of the medoids as the input to return the associations of non-medoid points 
    association=[]
    for i in range(1,len(data)):
        d=[]
        r=[]
        for k in range(0,5):
            if data[i,pos[k]]=='':
                d.append(data[pos[k],i])
            else:    
                d.append(data[i,pos[k]])
            
        for k in range(0,5):
            if min(d)==d[k]:
                r.append(data[i,0])
                r.append(data[0,pos[k]])
                association.append(r)
    return association
                

# Initial assciation of each non- medoid point to medoid centers has been done

 # note the first index is the same as the index of all the states in order in the data.csv file

# so we can store the indexes of the required points for further use

# function,forming the array containing the clusters, ini= medoids, association is the array input containing the asso. of each medoid
def clustering(ini,association):
    clus=[]
    for k in range(0,nk):
        buff=[]
        clus.append(ini[k])
        for i in range(0,30):
            if ini[k]==association[i][1]:
                buff.append(association[i][0])
        clus.append(buff) 
    return clus



# initial clustering done , now we start iterating so as to get the least cost solution
# algorithm step
# for each medoid
    #for each non-medoid
    #swap the datapoints to calculate the cost= sum of distances of the non-medoid points from the medoid center in each cluster

# now needed is the COST FUNCTION: calculates cost for a given input cluster 
#note that here the non-medoid array argument passed in the cost function contains the medoid as well, so we need to do a check
def cost(med,nmed):  
    c=0.0                                                 # med------ medoid , nmed---- non-medoid , c-- cost initialising
    med_idx=findpos([med],data)
    nmed_idx=findpos(nmed,data)                           # gives the positions of the datapoints in the data.csv file
    
    for m in range(0,len(nmed_idx)):
        if data[med_idx[0],nmed_idx[m]]=='':
            c=c+ float(data[nmed_idx[m],med_idx[0]])
        else:
            c=c+ float(data[med_idx[0],nmed_idx[m]])
        
    return c
# DONE

# <codecell>

# calculating the cost function for given set of clusters, using cost() and clus[] as input, which is the arrangement array of the different clusters
def costfun(clus):
    cf=0.0
    for i in range(0,len(clus),2):
        cf=cf+ cost(clus[i],clus[i+1])
    return cf 
# this gives the total cost of the current arrangement of clusters

# <codecell>

# Algorithm............
# Step SWAP
# Repeat until convergence:
#   Consider all pairs of objects (i, j) with
#   i ∈ {m1,...,mk} and j 6∈ {m1,...,mk}
#   and make the i ↔ j swap (if any) which decreases the objective most

# <codecell>
def finalcost(ini):
    ass=assoc(findpos(ini,data))
    cl=clustering(ini,ass)

    return costfun(cl)


# <codecell>
nk=5
cost_arr=[]
kappa=[]
for p in range(0,3):
    print p,cost_arr,len(cost_arr)
    ran=[]
    ini=[]# array storing unique random numbers
    while len(ran)<5:
        j=random.randint(0,29)
        if j in ran:
            continue
        else:
            ran.append(j)
        
    for i in range(0,len(ran)):
        ini.append(states[ran[i]])

    # medoids have been initialised..............
    print ini,finalcost(ini)
    
    if len(cost_arr)==0:
        cost_arr.append(finalcost(ini))
    elif finalcost(ini)<=cost_arr[-1]:
        cost_arr.append(finalcost(ini))
            


    
    for t in range(0,10000):
        d=random.randint(0,len(states)-1) # selecting a random non-medoid
        
        for i in range(0,nk):
            if states[d] not in ini:
                
                tmp=ini[i]
                ini[i]=states[d]    # swapping       
                pos=findpos(ini,data)
                association=assoc(pos)
                clus=clustering(ini,association)
                cost_s=costfun(clus)
                if cost_s<=cost_arr[-1]:
                    kappa.append(ini)
                    print 'found' , ini,finalcost(ini),'t=',t,'i=',i
                    cost_arr.append(cost_s)
                    
                    
                else:
                    ini[i]=tmp
                        
                        
                    
                        
            else:
                break







