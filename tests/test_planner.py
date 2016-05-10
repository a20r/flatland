
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import flatland
import matplotlib.pyplot as plt
import numpy as np
from ompl import geometric as og


def sanity_check():
    obs = flatland.RandomObstacleGen(dim=3, rad_mean=7).generate(30)
    start = np.array([-10, -10, -10])
    goal = np.array([10, 10, 10])
    planner = flatland.FLPlanner(
        dim=3, planner=og.PRMstar, obstacles=obs)
    planner.save_obstacles()
    res = planner.solve(start, goal, 1)
    res.write_to_file("sandbox/prmpath.txt")
    flatland.make_path_plot_3d()
    plt.show()


def sanity_check_dr():
    obs = flatland.RandomObstacleGen(dim=6).generate(10)
    start = np.array([-10, -10, -10, -10, -10, -10])
    goal = np.array([10, 10, 10, 10, 10, 10])
    planner = flatland.DRPlanner(
        high_dim=6, low_dim=4, planner=og.RRTstar, obstacles=obs)
    print planner.solve(start, goal)


if __name__ == "__main__":
    sanity_check()
