import numpy as np
import matplotlib.pyplot as plt
import pdb
import os

rrtPath = "sandbox/rrtpath.txt"
obstacleFolder = 'sandbox/obstacles/'

fig1 = plt.figure()

for i in os.listdir(obstacleFolder):
	obstaclePath = obstacleFolder + i

	with open(obstaclePath) as f:
		array = []
		for line in f: # read rest of lines
			array.append([float(x) for x in line.split()])

	pdb.set_trace()

	l = plt.plot(array[:,0],array[:,1],'r-')
	print array

with open(rrtPath) as f:
	array = []
	for line in f:
		array.append([float(x) for x in line.split()])

l = plt.plot(array[:,0],array[:,1],'b-')

plt.show()