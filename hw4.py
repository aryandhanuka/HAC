import csv
from scipy.cluster import hierarchy
import numpy as np
import matplotlib.pyplot as plt
import math

def load_data(filepath):
    #takes in a string with a path to the CSV file and returns the data points as a list of dicts
    myFile=open(filepath,'r')
    reader=csv.DictReader(myFile)
    myList=list()
    for dictionary in reader:
        myList.append(dictionary)
    return myList

def calc_features(row):
    #input: one row dict
    #calculate corresponding feature vector
    #return numPy array of shape(6,)-> dtype should be float64
    #pop,net migration, GDP,literacy,phones,infant mortality
    x=[0]*6
    x[0]=row["Population"]
    x[1]=row["Net migration"]
    x[2]=row["GDP ($ per capita)"]
    x[3]=row["Literacy (%)"]
    x[4]=row["Phones (per 1000)"]
    x[5]=row["Infant mortality (per 1000 births)"]
    x=np.asarray(x,dtype=np.float64)
    x=np.reshape(x,(6,))
    return x

def findMin(dist,n):
    #finds the minimum number in the upper right triangle of a square matrice
    #returns a tuple containing theminimum elements
    minr=-1
    minc=-1
    for row in range(0,n):
        for col in range(row+1,n):
            if minc==-1 and minr==-1 :
                if dist[row][col]!=0:
                    minc=col
                    minr=row
                else:
                    continue
            try:
                if dist[row][col]<dist[minr][minc] and dist[row][col]!=0:
                    minr=row
                    minc=col
                if dist[row][col]==dist[minr][minc]and dist[row][col]!=0:
                    #tie breaker rule: compare the first index and lowest index
                    rm=min(minr,minc)
                    cm=max(minr,minc)
                    r1=min(row,col)
                    c1=max(row,col)
                    if r1<rm or (r1==rm and c1<cm):
                        minr=row
                        minc=col
            except IndexError: 
                print(row)
                print(len(dist))
                print(col)
                print(len(dist[row]))
                exit()
    return (minr,minc)



def distance(x,y):
  return np.linalg.norm(x - y)




 #OUTPUT: numpy array of (4,n-1) shape
    #Each index is allocated as follows
    #Z[0]: index of the first cluster that is merged
    #Z[1]: index of the second cluster that was merged
    #Z[2]: the linkage distance between the two clusters that were merged
    #Z[3]: the size of the new cluster that was created
    #max D(A,B)-> D(set A,set B)
def hac(features):
    #create distance matrix
    n=len(features)
    dist = [[0 for _ in range(n)] for _ in range(n)] 
    for i in range(0,n):
        for k in range(0,n):
            dist[i][k]=distance(features[i],features[k])
    #end for loop
    #create empty numpy array of shape (n-1,4)
    z=np.empty(shape=(n-1,4),dtype=float)
    #now we must begin merging things
    k=n
    for index in range(n, n+n-1):
        #find new cluster to be merged
        x,y=findMin(dist,k)#x,y feature indexes/ z indexes 
        z[index-n][0]=min(x,y)
        z[index-n][1]=max(x,y)
        z[index-n][2]=dist[x][y]
        len1=1
        if x>=n:
            len1=z[x-n][3]
        len2=1
        if y>=n:
            len2=z[y-n][3]
        z[index-n][3]=len1+len2
        #update the distance matrix to reflect the newly added cluster
        #add new row and column at index k
        for row in range(0,k):
            #max of distance to X and distance to Y
            distX=dist[row][x]
            if row>x:
                distX=dist[x][row]
            distY=dist[row][y]
            if row>y:
                distY=dist[y][row]
            acd=max(distX,distY)
            dist[row].append(acd)
        k+=1
        dist.append([0]*k)
        #invalidate the rows and columns of the clusters that were used 
        for i in range(x+1,k):
            dist[x][i]=0
        for i in range(0,x):
            dist[i][x]=0
        for i in range(y+1,k):
            dist[y][i]=0
        for i in range(0,y):
            dist[i][y]=0 
    return z
def fig_hac(z,names):
    fig=plt.figure()
    hierarchy.dendrogram(z,labels=names, leaf_rotation=90)
    fig.tight_layout()
    return fig



def normalize_features5(features):
    a=list(map(float,[0]*6))*2
    for i in range(0,len(features)):
        for j in range(0,len(features[i])):
            a[0][j]+=features[i][j]
    for i in range(0,len(a[0])):
        a[0][i]/=len(features)
    #calculate the standard deviation of the values 
    for i in range(0,len(features)):
        for j in range(0,len(features[i])):
            deviation=pow(features[i][j]-a[0][j],2)
            a[1][j]=deviation
    for i in range(0,len(a[1])):
        a[1][i]/=len(features)
        a[1][i]=math.sqrt(a[1][i])
    print(a)
    for i in range(0,len(features)):
        for j in range(0,len(features[i])):
            features[i][j]-=a[0][j]
            features[i][j]/=a[1][j]
    return features

def normalize_features(features):
    mean=np.mean(a=features,axis=0)
    std=np.std(a=features,axis=0)
    for row in range(0,len(features)):
        for col in range(0,len(features[row])):
            features[row][col]-=mean[col]
            features[row][col]/=std[col]
    return features


