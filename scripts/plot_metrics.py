
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import warnings
from collections import defaultdict


planner_strs = ["RRTstar", "PRMstar"]
pl_clrs = {"RRTstar": "r", "PRMstar": "b"}
transformer_strs = ["FeatureAgglomeration", "TruncatedSVD",
                    "PCA", "KernelPCA", "RandomizedPCA"]

field_names = ["planner", "transformer", "n_collisions",
               "planning_duration", "path_length",
               "n_collisions_std", "planning_duration_std", "path_length_std",
               "num_failed"]


def load_data(filename):
    data = np.genfromtxt(filename, delimiter=",", dtype=None)[1:]
    planner_data = recursive_defaultdict(3, float)
    for row in data:
        for i in xrange(len(field_names) - 2):
            planner_data[row[0]][row[1]][field_names[i + 2]] = row[i + 2]
    return planner_data


def recursive_defaultdict(levels, dtype):
    return recursive_defaultdict_helper(defaultdict(dtype), levels - 1)


def recursive_defaultdict_helper(dd, level):
    new_dd = defaultdict(lambda: dd)
    if level == 1:
        return new_dd
    else:
        return recursive_defaultdict_helper(new_dd, level - 1)


def get_all(data, pl, key):
    xs = list()
    for tr in transformer_strs:
        xs.append(data[pl][tr][key])
    return xs


def make_plots(data, key):
    rects = list()
    fig, ax = plt.subplots()
    ind = np.arange(len(transformer_strs))
    width = 0.35
    for i, pl in enumerate(planner_strs):
        rect = ax.bar(
            ind + i * width, get_all(data, pl, key), width,
            color=pl_clrs[pl],
            label=pl)
        rects.append(rect)
        ax.set_ylabel(key)
    ax.set_xticks(ind + width)
    ax.set_xticklabels(transformer_strs)
    plt.legend()

if __name__ == "__main__":
    warnings.simplefilter("ignore")
    sns.set_context("poster", font_scale=2.2)
    data = load_data("data/data.csv")
    make_plots(data, "n_collisions")
    plt.show()
