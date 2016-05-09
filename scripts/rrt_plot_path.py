import numpy as np
import matplotlib.pyplot as plt
import os

rrtPath = "sandbox/prmpath.txt"
obstacleFolder = 'sandbox/obstacles/'

fig1 = plt.figure()

for i in os.listdir(obstacleFolder):
    obstaclePath = obstacleFolder + i

    with open(obstaclePath) as f:
        array = []
        for line in f:
            array.append([float(x) for x in line.split()])
            
    plt.plot(array[0], array[1], 'r-')
    print array

txt = np.loadtxt(rrtPath)
plt.plot(txt[:, 0], txt[:, 1], 'b-')

plt.show()
