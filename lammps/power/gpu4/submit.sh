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
srun -u --overlap --ntasks-per-node=1 --output "out-%J.log" ./gpubind0.sh hwloc-bind --cpubind core:32-39 -- ./monitor.sh &

srun -u --overlap --ntasks-per-node=1 --output "out-%J.log" ./gpubind0.sh hwloc-bind --cpubind core:0-7 -- lmp -in in.K_500 -log out.K_500_0.log &
j1=$!
srun -u --overlap --ntasks-per-node=1 --output "out-%J.log" ./gpubind0.sh hwloc-bind --cpubind core:8-15 -- lmp -in in.K_600 -log out.K_600_0.log &
j2=$!
srun -u --overlap --ntasks-per-node=1 --output "out-%J.log" ./gpubind0.sh hwloc-bind --cpubind core:16-23 -- lmp -in in.K_750 -log out.K_750_0.log &
j3=$!
srun -u --overlap --ntasks-per-node=1 --output "out-%J.log" ./gpubind0.sh hwloc-bind --cpubind core:24-31 -- lmp -in in.K_1000 -log out.K_1000_0.log &
j4=$!

wait $j1 $j2 $j3 $j4

sleep 10
touch stop_monitor

echo quit | nvidia-cuda-mps-control
