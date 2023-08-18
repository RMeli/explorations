import h5py
import numpy as np
import scipy
from matplotlib import pyplot as plt

N = 5120
batch_size = 1024


def load_tridiag(fname: str, name: str):
    """
    fname: str
        HDF5 file name
    name: str
        Name of the dataset
    """
    f = h5py.File(fname, "r")
    data = np.asarray(f[name]).squeeze(-1)

    d = data[0, :]
    t = data[1, :-1]

    assert d.shape == (N,)
    assert t.shape == (N - 1,)
    assert not np.any(np.isnan(d))
    assert not np.any(np.isnan(t))

    return d, t


def load_evals(fname: str, name: str):
    """
    fname: str
        HDF5 file name
    name: str
        Name of the dataset
    """
    f = h5py.File(fname, "r")

    e = np.asarray(f[name][0, :, 0])

    assert e.shape == (N,)

    if np.any(np.isnan(e)):
        print(f"Dataset '{name}' in '{fname}' contains NaNs!")

    return e


d, t = load_tridiag("data/tridiag-input-cp2k.h5", "tridiag")

e, ee = scipy.linalg.eigh_tridiagonal(d, t)
assert np.all(e[:-1] <= e[1:])  # sorted
assert not np.any(np.isnan(e))
assert not np.any(np.isnan(ee))

e_postbulk = load_evals(
    f"data/tridiag-output-evals-dlaf-bs{batch_size}-postbulk.h5", "evals"
)
e_prebulk = load_evals(
    f"data/tridiag-output-evals-dlaf-bs{batch_size}-prebulk.h5", "evals"
)

diff_postbulk = np.abs(e - e_postbulk)
diff_postbulk_sorted = np.abs(e - np.sort(e_postbulk))

diff_prebulk = np.abs(e - e_prebulk)
diff_prebulk_sorted = np.abs(e - np.sort(e_prebulk))

fig, axis = plt.subplots(1, 2)
plt.title(f"Unsorted (nb={batch_size})")
axis[0].plot(diff_postbulk)
axis[0].set_title("|NumPy - DLAF| (post-bulk)")
axis[1].plot(diff_prebulk)
axis[1].set_title("|NumPy - DLAF| (pre-bulk)")
plt.savefig("plots/diff.pdf")

fig, axis = plt.subplots(1, 2)
plt.title(f"Sorted (nb={batch_size})")
axis[0].plot(diff_postbulk_sorted)
axis[0].set_title("|NumPy - DLAF| (post-bulk)")
axis[1].plot(diff_prebulk_sorted)
axis[1].set_title("|NumPy - DLAF| (pre-bulk)")

plt.savefig("plots/diff-sorted.pdf")
