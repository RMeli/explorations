import argparse
import os

import h5py
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument("stage", choices=["eigensolver"])
parser.add_argument("steps", type=int)

args = parser.parse_args()


def is_same(a, b):
    return np.allclose(a, b)


def is_same_flipped(a, b):
    return is_same(a, -b)


for i in range(args.steps):
    with h5py.File(os.path.join("wrong", f"{args.stage}-{i}.h5")) as wrong, h5py.File(
        os.path.join("correct", f"{args.stage}-{i}.h5")
    ) as correct:

        def compare_dataset(dataset, flipped=False):
            c = correct[dataset][:].squeeze(-1)
            w = wrong[dataset][:].squeeze(-1)

            assert c.shape == w.shape

            # print(f"{dataset}: {c.shape}")

            if not is_same(c, w):
                if flipped and is_same_flipped(c, w):
                    print(f"Sign-flipped '{dataset}' for step {i}")
                else:
                    print(f"Different '{dataset}' for step {i}")

        compare_dataset("/input", flipped=True)
        compare_dataset("/evals")
        compare_dataset("/evecs", flipped=True)
