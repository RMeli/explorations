import argparse
import os

import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

df = pd.read_csv("data.csv")

y_labels = {
    "CP2K": "CP2K (s)",
    "cholesky": "Cholesky Decomposition (s)",
    "eigensolver": "Eigensolver (s)",
}

matrix_size = {
    "h2o-512": "20480",
    "h2o-1024": "40960",
}

# Consistency checks
e = df["total_energy"].dropna().to_numpy()
assert np.all(np.isclose(e, e[0]))


def lp(name, average=True):
    # Compute average over multiple function calls
    if average:
        df[name] /= df[f"n_{name}"]

    plt.figure()
    g = sns.lineplot(
        data=df,
        x="nodes",
        y=name,
        style="block_size",
        hue="la",
        markers=True,
        dashes=False,
        palette="colorblind",
    )
    g.set(xlabel="Nodes", ylabel=y_labels[name])
    g.legend(loc="center left", bbox_to_anchor=(1, 0.5))

    plt.gca().set_xscale("log", base=2)
    plt.gca().set_yscale("log", base=10)

    plt.tight_layout()

    for ext in ["png", "pdf"]:
        plt.savefig(f"{name}-elpa.{ext}")


lp("cholesky")
lp("eigensolver")
lp("CP2K", average=False)
