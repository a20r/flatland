
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import flatland
import numpy as np
from ompl import geometric as og


def sanity_check():
    obs = [np.array([[0, 0], [1, 0], [1, 0]])]
    planner = flatland.FLPlanner(10, og.PRMstar, obs)
    res = planner.solve()
    res.write_to_file("sandbox/prmpath.txt")


if __name__ == "__main__":
    sanity_check()
