from matplotlib import pyplot as plt
from matplotlib.ticker import NullFormatter, ScalarFormatter
from matplotlib.ticker import LogLocator
import seaborn as sns
import pandas as pd
import numpy as np

def load_and_pre_process(dlaf_version, pika_version, system, block_sizes_to_drop, nvgpu, amdgpu="Mi250x"):
    base = f"data/dlaf@{dlaf_version}-pika@{pika_version}"
    df = pd.read_csv(f"{base}/nvgpu_{system}.csv")
    try:
        df = pd.concat((df, pd.read_csv(f"{base}/amdgpu_{system}.csv")))
    except FileNotFoundError:
        # AMD GPUs are optional
        pass

    for bs in block_sizes_to_drop:
        df = df.drop(df[df.block_size == bs].index)

    e = df["total_energy"].dropna().to_numpy()
    assert np.all(np.isclose(e, e[0]))

    for old, new in {
        "dlaf-nvgpu": f"DLAF ({nvgpu})",
        "dlaf-amdgpu": f"DLAF ({amdgpu})",
        "elpa-nvgpu": f"ELPA ({nvgpu})",
    }.items():
        df.la = df.la.str.replace(old, new)

    df[['Library', 'Device']] = df['la'].str.split(expand=True)
    df['Device'] = df["Device"].str.replace("(", "")
    df['Device'] = df["Device"].str.replace(")", "")
    df = df.assign(ngpus=np.where(df.Device == nvgpu, 4, 8))
    df["ngpus"] = df["ngpus"] * df["nodes"]
    df = df.assign(ngpumodules=np.where(df.Device == nvgpu, 4, 4))
    df["ngpumodules"] = df["ngpumodules"] * df["nodes"]

    #df.rename(columns={"la": "Library", "block_size": "Block Size"}, inplace=True)
    df.drop(columns=["block_size", "la"], inplace=True)

    print(df)

    return df

df_clariden = load_and_pre_process("0.4.0", "0.22.1", "h2o-512", (512, 2048, 96), "A100")
df_santis = load_and_pre_process("git.pasc-2024-poster", "0.25.0", "h2o-512", (512, 2048, 96), "GH200")

def lp(df, name, cluster, ylims, average=False, legend=True):
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
    fig, ax = plt.subplots(figsize=(8.8 / 3, 3.6/2), gridspec_kw=dict(left=0.13, right=0.95, top=0.9, bottom=0.13))
    fig.set_facecolor([0]*4)

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
    if legend:
        g.legend(loc="upper right", ncol=2, prop={'size': 6})

    ax.set_xscale("log", base=2)
    ax.set_yscale("log", base=10)
    ax.set_xticks([1, 2, 4, 8], [1, 2, 4, 8])
    
    ax.grid(axis="y", linewidth=0.3)

    ax.get_yaxis().set_major_locator(LogLocator(10, [1, 2, 4, 7]))
    ax.get_yaxis().set_minor_locator(LogLocator(10, [1, 2, 3, 4, 5, 6, 7, 8, 9]))
    ax.get_yaxis().set_major_formatter(ScalarFormatter())
    ax.get_yaxis().set_minor_formatter(NullFormatter())
    plt.ylim(ylims)

    for ext in ["png", "pdf"]:
        fig.savefig(f"{name}-{cluster}.{ext}", bbox_inches="tight", dpi=600)


lp(df_clariden, "eigensolver", cluster="clariden", ylims=(120, 550))
lp(df_clariden, "CP2K", cluster="clariden", ylims=(275, 1100))

lp(df_santis, "eigensolver", cluster="santis", ylims=(120, 550))
lp(df_santis, "CP2K", cluster="santis", ylims=(275, 1100))
