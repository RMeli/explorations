from matplotlib import pyplot as plt
from matplotlib.ticker import NullFormatter, ScalarFormatter
from matplotlib.ticker import LogLocator
import seaborn as sns
import pandas as pd
import numpy as np

dlaf_version = "0.4.0"
pika_version = "0.22.1"
system = "h2o-512"
block_sizes_to_drop = [512, 2048, 96]

base = f"data/dlaf@{dlaf_version}-pika@{pika_version}"
df = pd.read_csv(f"{base}/nvgpu_{system}.csv")
df = pd.concat((df, pd.read_csv(f"{base}/amdgpu_{system}.csv")))

for bs in block_sizes_to_drop:
    df = df.drop(df[df.block_size == bs].index)

e = df["total_energy"].dropna().to_numpy()
assert np.all(np.isclose(e, e[0]))

for old, new in {
    "dlaf-nvgpu": "DLAF (A100)",
    "dlaf-amdgpu": "DLAF (Mi250x)",
    "elpa-nvgpu": "ELPA (A100)",
}.items():
    df.la = df.la.str.replace(old, new)

df[['Library', 'Device']] = df['la'].str.split(expand=True)
df['Device'] = df["Device"].str.replace("(", "")
df['Device'] = df["Device"].str.replace(")", "")
df = df.assign(ngpus=np.where(df.Device == "A100", 4, 8)) 
df["ngpus"] = df["ngpus"] * df["nodes"]
df = df.assign(ngpumodules=np.where(df.Device == "A100", 4, 4)) 
df["ngpumodules"] = df["ngpumodules"] * df["nodes"]

#df.rename(columns={"la": "Library", "block_size": "Block Size"}, inplace=True)
df.drop(columns=["block_size", "la"], inplace=True)

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

    #    title = f"{system.upper()} (dlaf@{dlaf_version}-pika@{pika_version})"
    title = "CP2K: H2O-512 (20480x20480)"

    #fig, ax = plt.subplots(figsize=(4.4, 2.2), gridspec_kw=dict(left=0.13, right=0.95, top=0.9, bottom=0.19))
    fig, ax = plt.subplots(figsize=(5, 4.3), gridspec_kw=dict(left=0.13, right=0.95, top=0.9, bottom=0.13))

    g = sns.lineplot(
        data=df,
        x="nodes",
        y=name,
        style="Device",
        hue="Library",
        markers=True,
        dashes=False,
        palette=["tab:red", "tab:orange"],
        ax=ax,
    )
    g.set(xlabel="Number of Nodes", ylabel=y_labels[name], title=title)
    g.legend(loc="upper right", ncol=2)

    ax.set_xscale("log", base=2)
    ax.set_yscale("log", base=10)
    
    ax.grid(axis="y", linewidth=0.3)

    ax.get_yaxis().set_major_locator(LogLocator(10, [1, 2, 4, 7]))
    ax.get_yaxis().set_minor_locator(LogLocator(10, [1, 2, 3, 4, 5, 6, 7, 8, 9]))
    ax.get_yaxis().set_major_formatter(ScalarFormatter())
    ax.get_yaxis().set_minor_formatter(NullFormatter())
#    plt.ylim(bottom=0)


    for ext in ["png", "pdf"]:
        fig.savefig(f"{name}.{ext}", bbox_inches="tight")


lp("eigensolver", average=False)
lp("CP2K", average=False)
