
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import flatland
import matplotlib.pyplot as plt
import numpy as np
from ompl import geometric as og


def sanity_check():
    obs = flatland.RandomObstacleGen().generate(100)
    start = np.array([-10, -10])
    goal = np.array([9, 9])
    planner = flatland.FLPlanner(
        dim=2, planner=og.RRTstar, obstacles=obs)
    res = planner.solve(start, goal, 10)
    res.write_to_file("sandbox/prmpath.txt")
    flatland.make_path_plot()
    plt.show()


if __name__ == "__main__":
    sanity_check()
