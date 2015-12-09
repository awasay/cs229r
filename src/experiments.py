import os
import rankedInsert as ri
import data as data
import math

n=1000
m=10000
k=10000
t=3
f="./results/datatype3_.csv"
start_e=0.01
start_b=10
d=0.01
e=0.1

b=start_b

# Calculate the number of iterations
iterations = 50*math.log(0.51*(n+1))
print "i " + str(iterations)
# Initialize sorted vectors
vectors,means = data.getSortedVectors(n,m,k,t)
# Initialize a random vector to be inserted in the sorted vectors
target_vector,target_mean = data.getRandomVector(m,k,t)



for i in range(0,10):
	b=pow(2,i)*10
	for j in range(0,1):
		ri.rankedInsert(vectors,means,target_vector,target_mean,b,iterations,f)
		