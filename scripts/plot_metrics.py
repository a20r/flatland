
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
import pandas
import sys


def prettify(text):
    words = text.split("_")
    return " ".join(w.capitalize() for w in words)


if __name__ == "__main__":
    warnings.simplefilter("ignore")
    sns.set_context("poster", font_scale=1.85)
    data = pandas.read_csv("data/data_final.csv")
    data.replace("FeatureAgglomeration", "F. Agg.", inplace=True)
    data.replace("RandomizedPCA", "R. PCA", inplace=True)
    hue = "n_obs"
    rrt = data[data["planner"] == "RRTConnect"]
    prm = data[data["planner"] == "PRM"]
    plt.subplot(3, 2, 1)
    ax = sns.barplot(x="transformer", y="path_length", hue=hue, data=rrt)
    ax.set(xlabel="")
    ax.set(ylabel="Path Length")
    ax.legend().remove()
    plt.title("RRTConnect")
    plt.subplot(3, 2, 2)
    ax = sns.barplot(x="transformer", y="path_length", hue=hue, data=prm)
    ax.set(ylabel="")
    ax.set(xlabel="")
    ax.legend().remove()
    plt.title("PRM")
    plt.subplot(3, 2, 3)
    ax = sns.barplot(x="transformer", y="duration", hue=hue, data=rrt)
    ax.set(ylabel="Duration")
    ax.set(xlabel="")
    ax.legend().remove()
    plt.subplot(3, 2, 4)
    ax = sns.barplot(x="transformer", y="duration", hue=hue, data=prm)
    ax.set(ylabel="")
    ax.set(xlabel="")
    ax.legend().remove()
    plt.subplot(3, 2, 5)
    ax = sns.barplot(x="transformer", y="num_failed", hue=hue, data=rrt)
    ax.set(ylabel="Num. Failed Runs",
           xlabel="Dimensionality Reduction Method")
    ax.legend(title="N. Obs.")
    plt.subplot(3, 2, 6)
    ax = sns.barplot(x="transformer", y="num_failed", hue=hue, data=prm)
    ax.set(ylabel="", xlabel="Dimensionality Reduction Method")
    ax.legend(title="N. Obs.")
    plt.show()
