
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import csv
import flatland
import numpy as np
import random
import sklearn.cluster as cluster
import sklearn.decomposition as decomp
from progressbar import ProgressBar, ETA, Percentage, Bar
from ompl import geometric as og
from collections import defaultdict


planners = [og.RRTstar, og.PRMstar]
transformers = [cluster.FeatureAgglomeration, decomp.TruncatedSVD,
                decomp.PCA, decomp.KernelPCA, decomp.RandomizedPCA]

planner_strs = ["RRTstar", "PRMstar"]
transformer_strs = ["FeatureAgglomeration", "TruncatedSVD",
                    "PCA", "KernelPCA", "RandomizedPCA"]

field_names = ["planner", "transformer", "n_collisions",
               "planning_duration", "path_length"]
n_obs = 10
n_runs = 100
high_dim = 6
low_dim = 4


def run_experiments(filename):
    with open(filename, "w") as f:
        writer = csv.DictWriter(f, fieldnames=field_names)
        writer.writeheader()
        max_num = len(transformers) * len(planners) * n_runs
        preface = "Running Experiments: "
        widgets = [preface, Bar(), Percentage(), "| ", ETA()]
        pbar = ProgressBar(widgets=widgets, maxval=max_num).start()
        counter = 0
        for i, tr in enumerate(transformers):
            for j, pl in enumerate(planners):
                row = dict()
                random.seed(0)
                data = defaultdict(list)
                for k in xrange(n_runs):
                    obs = flatland.RandomObstacleGen(dim=high_dim).generate(10)
                    start = -10 * np.ones((high_dim,))
                    goal = 10 * np.ones((high_dim,))
                    planner = flatland.DRPlanner(
                        high_dim=high_dim, low_dim=low_dim,
                        planner=og.RRTstar, obstacles=obs)
                    path, dur = planner.solve(start, goal)
                    data["n_collisions"].append(
                        planner.check_path(path))
                    data["planning_duration"].append(dur)
                    data["path_length"].append(path.shape[0])
                    pbar.update(counter)
                    counter += 1
                row["transformer"] = transformer_strs[i]
                row["planner"] = planner_strs[i]
                row["n_collisions"] = np.mean(data["n_collisions"])
                row["planning_duration"] = np.mean(data["planning_duration"])
                row["path_length"] = np.mean(data["path_length"])
                writer.writerow(row)


if __name__ == "__main__":
    run_experiments("data/data.csv")
