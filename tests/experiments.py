
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import csv
import flatland
import numpy as np
import random
import sklearn.cluster as cluster
import sklearn.decomposition as decomp
import scipy.spatial as spatial
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
               "planning_duration", "path_length",
               "n_collisions_std", "planning_duration_std", "path_length_std",
               "num_failed", "n_obs"]

n_obs = [30]
n_runs = 100
high_dim = 6
low_dim = 4
timeout = 1.5
rad_mean = 6.5


def run_experiments(filename):
    with open(filename, "w") as f:
        writer = csv.DictWriter(f, fieldnames=field_names)
        writer.writeheader()
        max_num = len(transformers) * len(planners) * n_runs * len(n_obs)
        preface = "Running Experiments: "
        widgets = [preface, Bar(), Percentage(), "| ", ETA()]
        pbar = ProgressBar(widgets=widgets, maxval=max_num).start()
        counter = 0
        for i, tr in enumerate(transformers):
            for j, pl in enumerate(planners):
                random.seed(0)
                for n_ob in n_obs:
                    row = dict()
                    data = defaultdict(list)
                    for k in xrange(n_runs):
                        try:
                            obs = flatland.RandomObstacleGen(
                                dim=high_dim).generate(n_ob)
                            start = -10 * np.ones((high_dim,))
                            goal = 10 * np.ones((high_dim,))
                            planner = flatland.DRPlanner(
                                high_dim=high_dim, low_dim=low_dim,
                                planner=og.RRTstar, obstacles=obs)
                            try:
                                path, dur = planner.solve(start, goal, timeout)
                                data["n_collisions"].append(
                                    planner.check_path(path))
                                data["planning_duration"].append(dur)
                                data["path_length"].append(path.shape[0])
                            except ValueError:
                                data["num_failed"].append(1)
                        except spatial.qhull.QhullError:
                            pass
                        pbar.update(counter)
                        counter += 1
                    row["transformer"] = transformer_strs[i]
                    row["n_obs"] = n_ob
                    row["planner"] = planner_strs[j]
                    row["n_collisions"] = np.mean(data["n_collisions"])
                    row["planning_duration"] = np.mean(data["planning_duration"])
                    row["path_length"] = np.mean(data["path_length"])
                    row["n_collisions_std"] = np.std(data["n_collisions"])
                    row["planning_duration_std"] = np.std(
                        data["planning_duration"])
                    row["path_length_std"] = np.std(data["path_length"])
                    row["num_failed"] = np.sum(data["num_failed"])
                    writer.writerow(row)


if __name__ == "__main__":
    run_experiments("data/data.csv")
