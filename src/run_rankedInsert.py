import numpy as np
import argparse
import math
import os.path
import sys

import data as data
import rankedInsert as ri

#####
## Param ##


parser = argparse.ArgumentParser()


parser.add_argument('-b', help='budget for each iteration')
parser.add_argument('-n', help='number of vectors')
parser.add_argument('-m', help='size of vectors')
parser.add_argument('-k', help='max value in vectors')
parser.add_argument('-t', help='type of data (1,2 or 3)')



args = parser.parse_args()

n=int(args.n)
m=int(args.m)
k=int(args.k)
t=int(args.t)
b=int(args.b)

if len(sys.argv) != 11:
	print "Incomplete arguments, type 'python run_ranked_insert.py -h' "
	exit()


# Calculate the budget:
budget = b

# Calculate the number of iterations
iterations = 50*math.log(0.51*(n+1))

print "Number of vectors " + str(n)
print "Size of vectors " + str(m)
print "Maximum number of vectors " + str(k)
print "Type of data " + str(t)
print "Budget " + str(b)
print "Number of iterations "+str(iterations)
print "** ** ** "

# Initialize sorted vectors
vectors,means = data.getSortedVectors(n,m,k,t)

# Initialize a random vector to be inserted in the sorted vectors
target_vector,target_mean = data.getRandomVector(m,k,t)

ri.rankedInsert(vectors,means,target_vector,target_mean,budget,iterations,"runs")
exit()
