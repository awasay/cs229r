import numpy as np
import argparse
import math
import os.path

import data as data
import plot as plot
import rankedInsert as ri

#####
## Param ##

parser = argparse.ArgumentParser()
parser.add_argument('-e', help='epsilon')
parser.add_argument('-d', help='delta')
parser.add_argument('-b', help='budget')

parser.add_argument('-n', help='number of vectors')
parser.add_argument('-m', help='size of vectors')
parser.add_argument('-k', help='max value in vectors')
parser.add_argument('-f', help='filename')
parser.add_argument('-t', help='type of data')

args = parser.parse_args()

e=float(args.e)
d=float(args.d)
n=int(args.n)
m=int(args.m)
k=int(args.k)
f=args.f
t=int(args.t)
b = int(args.b)



print "e,d,n,m,k,t"
print e,d,n,m,k,t

# Calculate the budget:
#budget = math.log(1.0/(d*e*e),2)
budget = b
print "b " + str(budget)


# Calculate the number of iterations
iterations = 50*math.log(0.51*(n+1))
print "i " + str(iterations)


# Initialize sorted vectors
vectors,means = data.getSortedVectors(n,m,k,t)
# Initialize a random vector to be inserted in the sorted vectors
target_vector,target_mean = data.getRandomVector(m,k,t)

ri.rankedInsert(vectors,means,target_vector,target_mean,budget,iterations,f)
exit()

# Initialize weights associated with the interval v_i and v_i+1 
weights=[]
pivots=[]
ri.initializeWeights(weights,vectors)
assert(len(weights)==len(vectors)+1)


#print "* * *"
print "exact position " + str(np.searchsorted(means,target_mean))
#print "number of vectors " + str(len(vectors))
#print "size of vectors " + str(len(vectors[0]))
#print "* * *"

for i in range(0,int(iterations)):

	# Find the pivot: the maximum i where the sum of the weights < 0.5
	pivot_sum, pivot = ri.findPivot(weights)
	
	if pivot_sum==-1 or pivot==-1:
		break

	# Flip a coin and pick pivot or pivot+1
	pivot = ri.pick(pivot,pivot+1)
	pivots.append(pivot)

	# Estimate the mean of the pivot vector
	estimate_pivot_mean = ri.estimateMean(vectors[pivot],budget)
	
	# Update the weights based on the estimate of the mean
	if target_mean < estimate_pivot_mean:
		ri.updateWeights(weights,0,pivot-1,3.0/(2.0+pivot_sum))
		ri.updateWeights(weights,pivot,len(weights),2.0/(2.0+pivot_sum))
	elif target_mean > estimate_pivot_mean:
		ri.updateWeights(weights,0,pivot-1,2.0/(3.0-pivot_sum))
		ri.updateWeights(weights,pivot,len(weights),3.0/(3.0-pivot_sum))

	#print "iteration " + str(i)
	#print "pivot " + str(pivot)
	#print "budget " + str(int(1.0/epsilon))
	#print "estimate pivot mean " + str(estimate_pivot_mean)
	#print "actual pivot mean " + str(means[pivot])
	#print "difference " + str(estimate_pivot_mean - means[pivot])
	#print "sum of weights " + str(sum(weights))
	#print "**"	
	
actual_answer = np.searchsorted(means,target_mean)[0]
alg_answer = np.argmax(weights)
difference_mean = min(means[alg_answer]-means[actual_answer],means[alg_answer+1]-means[actual_answer])
difference_posn = abs(actual_answer - alg_answer)
print "**"
print "alg answer " + str(alg_answer)
print "answer actual " + str(actual_answer)
print "mean [i] " + str(means[alg_answer])
print "mean [i+1] " + str(means[alg_answer+1])
print "mean [actual answer]" + str(means[actual_answer])
print "difference in mean " + str(difference_mean)
print "difference in position " + str(difference_posn)
#print "answer median(pivots) " + str(np.median(pivots))

# Store in values that you want to plot

if not os.path.isfile(f):
	outfile = open(f,'a')
	outfile.write("budget, difference in mean, difference in position, max value, total vectors \n")		
else:
	outfile = open(f,'a')
outfile.write(str(budget)+","+str(difference_mean)+","+str(difference_posn)+","+str(k)+str(n)+"\n")

#plot.PlotSimple(f,"budget",["difference in mean","difference in position"],f+"_plot",1)


