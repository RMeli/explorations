from matplotlib import pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

version = "0.3.1"
system = "h2o-512"
block_sizes_to_drop = [512, 2048, 96]

df = pd.read_csv(f"data/dlaf@{version}/nvgpu_{system}.csv")
df = pd.concat((df, pd.read_csv(f"data/dlaf@{version}/amdgpu_{system}.csv")))

for bs in block_sizes_to_drop:
    df = df.drop(df[df.block_size == bs].index)

e = df["total_energy"].dropna().to_numpy()
assert np.all(np.isclose(e, e[0]))

for old, new in {
    "dlaf-nvgpu": "DLAF (A100)",
    "dlaf-amdgpu": "DLAF (Mi200)",
    "elpa-nvgpu": "ELPA (A100)",
}.items():
    df.la = df.la.str.replace(old, new)

df.rename(columns={"la": "Library", "block_size": "Block Size"}, inplace=True)

print(df)


def lp(name, average=True):
    y_labels = {
        "CP2K": "CP2K (s)",
        "cholesky": "Cholesky Decomposition (s)",
        "eigensolver": "Eigensolver (s)",
    }

    # Compute average over multiple function calls
    if average:
        df[name] /= df[f"n_{name}"]

    title = f"{system.upper()} (dlaf@{version})"

    plt.figure()
    g = sns.lineplot(
        data=df,
        x="nodes",
        y=name,
        style="Block Size",
        hue="Library",
        markers=True,
        dashes=False,
        palette="colorblind",
    )
    g.set(xlabel="Nodes", ylabel=y_labels[name], title=title)
    g.legend(loc="center left", bbox_to_anchor=(1, 0.5))

    plt.gca().set_xscale("log", base=2)

    plt.ylim(bottom=0)

    plt.tight_layout()

    for ext in ["png", "pdf"]:
        plt.savefig(f"{name}.{ext}")


lp("eigensolver", average=False)
lp("CP2K", average=False)
