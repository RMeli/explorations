import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

df = pd.read_csv("results.csv")

unit = df.units.unique().item()

x_name = "Number of Daint@ALPS Nodes"
y_name = f"SIRIUS Runtime ({unit})"

df.rename(columns={"nodes": x_name, "time": y_name, "library": "Eigensolver"}, inplace=True)
df.replace(to_replace={"dlaf": "DLAF (1024)", "elpa1": "ELPA1 (128)", "elpa2": "ELPA2 (128)", "cusolver": "cuSOLVER"}, inplace=True)

fig, ax = plt.subplots(figsize=(3.5, 3))
plot = sns.lineplot(data=df, x=x_name, y=y_name, hue="Eigensolver", style="Eigensolver", markers=True, dashes=False, ax=ax)
plot.set_title("SIRIUS FP-LAPWlo for C60 (18'559)")

ax.set_xscale("log")

ax.set_xticks(ticks=[0.25, 0.5, 1, 2, 4, 8], labels=["1/4", "1/2", "1", "2", "4", "8"])

fig.tight_layout()

fig.savefig("sirius.png")
fig.savefig("sirius.pdf")