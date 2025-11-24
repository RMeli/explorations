import argparse as ap

import h5py
import numpy as np
import scipy

parser = ap.ArgumentParser()
parser.add_argument("matrix_size", type=int, help="Matrix size")
parser.add_argument("last_eval_index", type=int, help="Last eigenvalue index")
parser.add_argument("problem", type=str, choices=("std", "gen"), help="Eigenvalue problem type")
args = parser.parse_args()

N = args.matrix_size
last_eval_index = args.last_eval_index

np.set_printoptions(linewidth=250, suppress=True)


def load_input(fname: str, name: str):
    """
    fname: str
        HDF5 file name
    name: str
        Name of the dataset
    """
    f = h5py.File(fname, "r")
    a = np.asarray(f[name]).squeeze(-1)

    assert a.shape == (N, N), a.shape
    assert scipy.linalg.ishermitian(a)

    return a.T


def load_evals(fname: str, name: str):
    """
    fname: str
        HDF5 file name
    name: str
        Name of the dataset
    """
    f = h5py.File(fname, "r")

    e = np.asarray(f[name][0, :, 0])

    assert e.shape == (N,), e.shape

    if np.any(np.isnan(e)):
        print(f"Dataset '{name}' in '{fname}' contains NaNs!")

    return e


def load_evecs(fname: str, name: str):
    """
    fname: str
        HDF5 file name
    name: str
        Name of the dataset
    """
    f = h5py.File(fname, "r")
    ee = np.asarray(f[name]).squeeze(-1)

    assert ee.shape == (N, N), ee.shape

    return ee.T


datafile = f"data/{args.problem}/n{N}-e{last_eval_index}.h5"

a = load_input(datafile, "input" + "-a" if args.problem == "gen" else "")
if args.problem == "gen":
    b = load_input(datafile, "input-b")
e = load_evals(datafile, "evals")
ee = load_evecs(datafile, "evecs")

# Solve with SciPy
e_scipy, ee_scipy = scipy.linalg.eigh(a) if args.problem == "std" else scipy.linalg.eigh(a, b)
assert np.all(e_scipy[:-1] <= e_scipy[1:])  # sorted
assert not np.any(np.isnan(e_scipy))
assert not np.any(np.isnan(ee_scipy))

diff = np.abs(e - e_scipy)
assert np.allclose(diff, 0.0, atol=1e-12)

num_evals = last_eval_index + 1

print(f"Number of eigenvalues: {num_evals}")
print(f"Eigenvalue range: (0, {last_eval_index})")
print("dla-future:\t", e)
print("scipy:\t\t", e_scipy)
print("dla-future:\n", ee)
print("scipy:\n", ee_scipy)

# Check that evecs are the same in range (0, last_eval_index)
for i in range(num_evals):
    diff1 = np.abs(ee[:, i] - ee_scipy[:, i])
    diff2 = np.abs(ee[:, i] + ee_scipy[:, i])
    assert np.allclose(diff, 0.0, atol=1e-12) or np.allclose(diff2, 0.0, atol=1e-12)

# Check that evecs are different in range (last_eval_index + 1, N)
for i in range(num_evals, N):
    diff1 = np.abs(ee[:, i] - ee_scipy[:, i])
    diff2 = np.abs(ee[:, i] + ee_scipy[:, i])
    assert not np.allclose(diff1, 0.0, atol=1e-12), diff1
    assert not np.allclose(diff2, 0.0, atol=1e-12), diff2
