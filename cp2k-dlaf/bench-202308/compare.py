import argparse
import os

import h5py
import numpy as np
from matplotlib import pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument("stage", choices=["eigensolver"])
parser.add_argument("steps", type=int)
parser.add_argument("--plot-evecs", default=False, action="store_true")

args = parser.parse_args()


def is_same(a, b):
    return np.allclose(a, b)


def is_same_flipped(a, b):
    return is_same(a, -b)


def plot_evecs(dataset, c, w, i):
    if "evecs" in dataset:
        fig, (ax1, ax2) = plt.subplots(figsize=(8, 4), ncols=2)
        p = ax1.imshow(c, interpolation="none")
        ax1.set_title("Correct")
        fig.colorbar(p, ax=ax1)
        p = ax2.imshow(w, interpolation="none")
        ax2.set_title("Wrong")
        fig.colorbar(p, ax=ax2)
        plt.savefig(f"eigenvectors-{i}.pdf")


for i in range(args.steps):
    with h5py.File(os.path.join("wrong", f"{args.stage}-{i}.h5")) as wrong, h5py.File(
        os.path.join("correct", f"{args.stage}-{i}.h5")
    ) as correct:

        def compare_dataset(dataset, flipped=False):
            c = correct[dataset][:].squeeze(-1)
            w = wrong[dataset][:].squeeze(-1)

            assert c.shape == w.shape

            if not is_same(c, w):
                if flipped and is_same_flipped(c, w):
                    print(f"Sign-flipped '{dataset}' for step {i}")
                else:
                    print(f"Different '{dataset}' for step {i}")

                    if args.plot_evecs:
                        plot_evecs(dataset, c, w, i)

        compare_dataset("/input")
        compare_dataset("/evals")
        compare_dataset("/evecs", flipped=True)
