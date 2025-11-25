#!/bin/bash
#SBATCH --job-name=lammps-metatomic
#SBATCH --time=00:30:00
#SBATCH --account=csstaff
#SBATCH --nodes=1
#SBATCH --uenv=lammps-metatomic/rc2:2064644445@daint
#SBATCH --view=lammps
#SBATCH --exclusive --mem=450G

export CUDA_MPS_PIPE_DIRECTORY=/tmp/nvidia-mps
export CUDA_MPS_LOG_DIRECTORY=/tmp/nvidia-log-$(id -un)
CUDA_VISIBLE_DEVICES=0,1,2,3 nvidia-cuda-mps-control -d
sleep 1

rm -f stop_monitor

srun -u --overlap --ntasks-per-node=1 --output "out-%J.log" hwloc-bind --cpubind core:8-15 -- ./monitor.sh &

srun -u --overlap --ntasks-per-node=1 --output "out-%J.log" ./gpubind0.sh hwloc-bind --cpubind core:0-7 -- lmp -in in.K_500 -log none -k on g 1 -sf kk -pk kokkos neigh half  &
pidj1=$!

wait $pidj1

sleep 10
touch stop_monitor

echo quit | nvidia-cuda-mps-control
