
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import flatland
from ompl import geometric as og


def sanity_check():
    planner = flatland.FLPlanner(8, og.PRMstar)
    res = planner.solve()
    res.write_to_file("sandbox/prmpath.txt")


if __name__ == "__main__":
    sanity_check()
