import numpy as np
import random
import os

def estimateMean(vector,budget):
	
	# Take a random sample of size = epsilon

	if budget >= len(vector):
		budget = len(vector)

	temp = np.arange(len(vector))
	np.random.shuffle(temp)
	sample_index = temp[0:budget]
	sample = vector[sample_index]

	return np.mean(sample)

def initializeWeights(weights,vectors):

	num=len(vectors)

	# Initialize weights

	for i in range(0,num+1):
		weights.append(float(1.0/(num+1)))

# Update weights from start to end (exclusive) by w=w*multiplier

def updateWeights(weights,start,end,multiplier):

	for i in range(start,end):
		weights[i]=weights[i]*multiplier

def findPivot(weights):
	
	sum=0.0

	for i in range(0,len(weights)):
		sum=sum+weights[i]
		if sum >= 0.5:
			return sum-weights[i]-weights[i-1], i-1
	return -1,-1

def pick(a,b):
	
	coin = random.randint(0,1)
	
	if coin == 1:
		return a
	
	if coin == 0:
		return b
	
	return -1

def rankedInsert(vectors,means,target_vector,target_mean,budget,iterations,f):

# Initialize weights associated with the interval v_i and v_i+1 
	weights=[]
	pivots=[]
	initializeWeights(weights,vectors)
	assert(len(weights)==len(vectors)+1)

	for i in range(0,int(iterations)):

		# Find the pivot: the maximum i where the sum of the weights < 0.5
		pivot_sum, pivot = findPivot(weights)
		
		# # # #
		if pivot_sum==-1 or pivot==-1 or pivot > len(vectors)-2:
			continue

		# Flip a coin and pick pivot or pivot+1
		pivot = pick(pivot,pivot+1)

		# Keep track of the pivots
		pivots.append(pivot)

		# Estimate the mean of the pivot vector using the given budget
		estimate_pivot_mean = estimateMean(vectors[pivot],budget)
		
		# Update the weights based on the estimate of the mean
		if target_mean < estimate_pivot_mean:
			updateWeights(weights,0,pivot-1,3.0/(2.0+pivot_sum))
			updateWeights(weights,pivot,len(weights),2.0/(2.0+pivot_sum))
		elif target_mean > estimate_pivot_mean:
			updateWeights(weights,0,pivot-1,2.0/(3.0-pivot_sum))
			updateWeights(weights,pivot,len(weights),3.0/(3.0-pivot_sum))

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

	# Store in values that you want to plot

	if not os.path.isfile(f):
		outfile = open(f,'a')
		outfile.write("budget, difference in mean,difference in position,total vectors \n")		
	else:
		outfile = open(f,'a')
	outfile.write(str(budget)+","+str(difference_mean)+","+str(difference_posn)+","+str(len(vectors))+"\n")









