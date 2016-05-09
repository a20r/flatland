import numpy as np
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches
import os
import pdb


rrtPath = "sandbox/prmpath.txt"
obstacleFolder = 'sandbox/obstacles/'


def generate_codes(length):
	codes = list()
	codes.append(Path.MOVETO)
	for _ in xrange(1, length - 1):
		codes.append(Path.LINETO)
	codes.append(Path.STOP)
	return codes


def make_path_plot():
	fig1 = plt.figure()

	for i in os.listdir(obstacleFolder):
	    obstaclePath = obstacleFolder + i

	    ob = np.loadtxt(obstaclePath)
	    ob = np.vstack((ob, ob[0, :]))
	    path = Path(ob)
	    patch = patches.PathPatch(path, facecolor='orange', lw=2)
	    ax = plt.gca()
	    ax.add_patch(patch)

	txt = np.loadtxt(rrtPath)
	plt.plot(txt[:, 0], txt[:, 1], 'b-')


if __name__ == "__main__":
	make_path_plot()
	plt.show()