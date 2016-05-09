
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import flatland
import numpy as np
from ompl import geometric as og


def sanity_check():
    obs = [np.array([[0, 0], [1, 0], [1, 0]])]
    start = np.array([0, 0])
    goal = np.array([3, 3])
    planner = flatland.FLPlanner(
        dim=2, planner=og.PRMstar, obstacles=obs)
    res = planner.solve(start, goal)
    res.write_to_file("sandbox/prmpath.txt")


if __name__ == "__main__":
    sanity_check()
