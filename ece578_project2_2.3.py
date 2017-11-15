import random
import unittest
import scipy.io 

from scipy.io.matlab import loadmat as load
import numpy as np


def main(datfile="20170901.as-rel2.txt"):
    outarr = []
    with open(datfile) as datafd:
        for line in datafd:
            if not line.startswith("#"):
                outarr.append( [int(val) for val in line.split("|")[:-1] ] )

    return np.array( outarr )









def rank_by_degree(rawdata):
    degree = np.array(np.unique(rawdata[:,0], return_counts=True)).transpose()
    reverse_sorted = degree[ degree[:,1].argsort() ]
    degsort = np.flipud(reverse_sorted)
    
    return degsort


        

def largest_clique(ASdata, DegData):
    
    SS=set()
    for AS in DegData[:,0]:
        break



def isConnected(AS0, AS1, ASdata):
    AS0s = np.where(ASdata[:,0] == AS0)[0]
    for row in AS0s:
        if AS1 == ASdata[ row, 1 ]:
            print row
            return True

    AS1s = np.where( ASdata[:, 1] == AS1 )[0]
    for row in AS1s:
        if AS0 == ASdata[ row, 1 ]:
            print row
            return True


    return False


    


