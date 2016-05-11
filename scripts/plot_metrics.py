
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import warnings
import pandas


if __name__ == "__main__":
    warnings.simplefilter("ignore")
    sns.set_context("poster", font_scale=1)
    data = pandas.read_csv("data/data.csv")
    hue = "n_obs"
    rrt = data[data["planner"] == "RRTConnect"]
    prm = data[data["planner"] == "PRM"]
    plt.subplot(3, 2, 1)
    ax = sns.barplot(x="transformer", y="path_length", hue=hue, data=rrt)
    ax.set(xlabel="")
    plt.title("RRTConnect")
    plt.subplot(3, 2, 2)
    ax = sns.barplot(x="transformer", y="path_length", hue=hue, data=prm)
    ax.set(xlabel="")
    plt.title("PRM")
    plt.subplot(3, 2, 3)
    ax = sns.barplot(x="transformer", y="duration", hue=hue, data=rrt)
    ax.set(xlabel="")
    plt.subplot(3, 2, 4)
    ax = sns.barplot(x="transformer", y="duration", hue=hue, data=prm)
    ax.set(xlabel="")
    plt.subplot(3, 2, 5)
    sns.barplot(x="transformer", y="num_failed", hue=hue, data=rrt)
    plt.subplot(3, 2, 6)
    sns.barplot(x="transformer", y="num_failed", hue=hue, data=prm)
    plt.show()
