import numpy as np
import math
import os

import rankedInsert as ri
import data as data
import rankedInsert as ri

def jaccard(im1, im2):
	intesection = np.intersect1d(im1,im2)
	union = np.union1d(im1,im2)


	return len(intesection)*1.0/len(union)*1.0


def getActualTopK(means):
	return np.argsort(means)

def insertSentinels(vectors,means):
	
	vectors_length = len(vectors) 

	new_vectors = []
	new_means = []

	new_vectors.append(np.zeros(vectors_length))
	new_vectors.extend(vectors)
	new_vectors.append(np.ones(vectors_length)*100000)

	new_means.append(0)
	new_means.extend(means)
	new_means.append(100000)

	return new_vectors,new_means

def rankedInsert(vectors,means,target_vector,target_mean,budget,iterations,f):

	# Initialize weights associated with the interval v_i and v_i+1 
	weights=[]
	pivots=[]
	ri.initializeWeights(weights,vectors)
	assert(len(weights)==len(vectors)+1)

	for i in range(0,int(iterations)):

		# Find the pivot: the maximum i where the sum of the weights < 0.5
		pivot_sum, pivot = ri.findPivot(weights)
		
		if pivot_sum==-1 or pivot==-1 or pivot > len(vectors)-2:
			continue

		# Flip a coin and pick pivot or pivot+1
		pivot = ri.pick(pivot,pivot+1)

		# Keep track of the pivots
		pivots.append(pivot)

		# Estimate the mean of the pivot vector using the given budget
		estimate_pivot_mean = ri.estimateMean(vectors[pivot],budget)
		
		# Update the weights based on the estimate of the mean
		if target_mean < estimate_pivot_mean:
			ri.updateWeights(weights,0,pivot-1,3.0/(2.0+pivot_sum))
			ri.updateWeights(weights,pivot,len(weights),2.0/(2.0+pivot_sum))
		elif target_mean > estimate_pivot_mean:
			ri.updateWeights(weights,0,pivot-1,2.0/(3.0-pivot_sum))
			ri.updateWeights(weights,pivot,len(weights),3.0/(3.0-pivot_sum))

	actual_answer = np.searchsorted(means,target_mean)
	alg_answer = np.argmax(weights)
	difference_mean = min(means[alg_answer]-means[actual_answer],means[alg_answer+1]-means[actual_answer])
	difference_posn = abs(actual_answer - alg_answer)
	return alg_answer

def topk(vectors,means,k,budget,iterations,f):

	alg_vectors=[]
	alg_means=[]

	alg_means.append(means[0])
	alg_vectors.append(vectors[0])
	alg_vectors,alg_means = insertSentinels(alg_vectors,alg_means)	


	for i in range(1,len(vectors)):
		calculated_position = rankedInsert(alg_vectors,alg_means,vectors[i],means[i],budget,iterations,"run")
		alg_vectors.insert(calculated_position+1,vectors[i])
		alg_means.insert(calculated_position+1,means[i])

	estimate = alg_means[0:k]
	actual = np.sort(alg_means)[0:k]

	# Error metrics

	jcrd=str(jaccard(estimate,actual))
	sum_mean_difference=math.fabs(sum(actual)-sum(estimate))
	fractional_sum_mean_difference=str(float(sum_mean_difference)/np.sum(actual))

	#print estimate 
	#print actual

	print "Jaccard index between top-k_actual and top-k_estimate " + jcrd
	print "The fractional error in the sum of means between top-k_actual and top-k_estimate " + fractional_sum_mean_difference
	if not os.path.isfile(f):
		outfile = open(f,'a')
		outfile.write("b, Jaccard, fractional error in the sum of means\n")		
	else:
		outfile = open(f,'a')
	outfile.write(str(budget)+","+jcrd+","+fractional_sum_mean_difference+"\n")
	

def calculateSetDifference(estimate,actual):
	return len(np.setdiff1d(estimate,actual))

