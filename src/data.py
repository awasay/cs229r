import numpy as np
import random

def generateVectors(num,size,max,type):

	vectors=[]
	means=[]
	start=0

	if num >= 2:
		vectors.append(np.zeros(size))
		vectors.append(np.ones(size)*max)
		means.append(0)
		means.append(max)
		start=2
	
	# Type : 1 uniform data within the same interval
	if type == 1:
		for i in range(start,num):
			vectors.append(np.random.uniform(0,max,size))
			means.append(np.mean(vectors[i]))
	
	# Type : 2 uniform data within random intervals
	if type == 2:
		for i in range(start,num):
			vectors.append(np.random.uniform(random.randint(0,max/2),random.randint(max/2,max),size))
			means.append(np.mean(vectors[i]))

	#Type : 3 uniform data with non-overlapping intervals
	if type == 3:
		intervals = max/num
		for i in range(start,num):
			vectors.append(np.random.uniform(intervals*i,intervals*(i+1),size))
			means.append(np.mean(vectors[i]))

	return vectors,means 

def rearrange(lst,order):
	assert(len(lst)==len(order))

	temp_list=[]

	for i in range(0,len(order)):
		temp_list.append(lst[order[i]])

	return temp_list

def sortVectors(vectors,means):
	
	sort_order = np.argsort(means)
	vectors = rearrange(vectors,sort_order)
	means = rearrange(means,sort_order)
	
	return vectors,means

def getSortedVectors(num,size,max,type):

	vectors,means = generateVectors(num,size,max,type)
	vectors,means = sortVectors(vectors,means)
	return vectors,means

def getRandomVector(size,max,type):

	return generateVectors(1,size,max,type)
