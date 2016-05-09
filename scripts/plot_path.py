import numpy as np
import matplotlib.pyplot as plt
import os
import pdb

rrtPath = "sandbox/prmpath.txt"
obstacleFolder = 'sandbox/obstacles/'

fig1 = plt.figure()

for i in os.listdir(obstacleFolder):
    obstaclePath = obstacleFolder + i

    ob = np.loadtxt(obstaclePath)
    plt.plot(ob[:,0],ob[:,1],'r-')


txt = np.loadtxt(rrtPath)
plt.plot(txt[:, 0], txt[:, 1], 'b-')

plt.show()