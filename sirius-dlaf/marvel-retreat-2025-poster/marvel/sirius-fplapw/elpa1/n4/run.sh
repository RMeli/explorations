#!/bin/bash -l
#SBATCH --job-name=sirius
#SBATCH --time=00:30:00
#SBATCH --nodes=4
#SBATCH --ntasks-per-node=4
#SBATCH --hint=multithread
#SBATCH --no-requeue
#SBATCH --cpus-per-task=64
#SBATCH --uenv=/capstor/scratch/cscs/rmeli/squashfs/sirius-7.6.1-dlaf-0.7.3.squashfs:/user-environment/

uenv view sirius

export FI_MR_CACHE_MONITOR=disabled
export MPICH_GPU_SUPPORT_ENABLED=1
export MIMALLOC_EAGER_COMMIT_DELAY=0
export MIMALLOC_ALLOW_LARGE_OS_PAGES=1
export DLAF_BT_BAND_TO_TRIDIAG_HH_APPLY_GROUP_SIZE=128
export DLAF_UMPIRE_DEVICE_MEMORY_POOL_ALIGNMENT_BYTES=$((1 << 21))

export OMP_NUM_THREADS=$((SLURM_CPUS_PER_TASK - 1))

srun -u --gpus-per-task=1 --cpu-bind=verbose,core -c ${SLURM_CPUS_PER_TASK} sirius.scf --control.mpi_grid_dims=4:4
