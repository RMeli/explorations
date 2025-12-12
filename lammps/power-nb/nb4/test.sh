#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=4
#SBATCH --gpus-per-task=1
#SBATCH --time=00:20:00
#SBATCH --uenv=prgenv-gnu/25.6:v2
#SBATCH --view=default

rm -f stop_monitor
date

export CUDA_MPS_PIPE_DIRECTORY=/tmp/nvidia-mps
export CUDA_MPS_LOG_DIRECTORY=/tmp/nvidia-log-$(id -un)
CUDA_VISIBLE_DEVICES=0,1,2,3 nvidia-cuda-mps-control -d
sleep 1

srun --overlap -n1 monitor.sh &
pid=$!
sleep 30

srun --overlap -n1 ./gpubind0.sh hwloc-bind --cpubind core:0-7 -- ../node-burn/build/burn -ggemm,5000 -d900 & 
pidj11=$!
srun --overlap -n1 ./gpubind0.sh hwloc-bind --cpubind core:8-15 -- ../node-burn/build/burn -ggemm,5000 -d900 & 
pidj12=$!
srun --overlap -n1 ./gpubind0.sh hwloc-bind --cpubind core:16-23 -- ../node-burn/build/burn -ggemm,5000 -d900 & 
pidj13=$!
srun --overlap -n1 ./gpubind0.sh hwloc-bind --cpubind core:24-31 -- ../node-burn/build/burn -ggemm,5000 -d900 & 
pidj14=$!

wait $pidj11 $pidj12 $pidj13 $pidj14

sleep 30
touch stop_monitor
wait $pid

echo quit | nvidia-cuda-mps-control

date
