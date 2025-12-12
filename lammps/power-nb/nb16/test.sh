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

srun --overlap -n1 ./gpubind1.sh hwloc-bind --cpubind core:72-79 -- ../node-burn/build/burn -ggemm,5000 -d900 & 
pidj21=$!
srun --overlap -n1 ./gpubind1.sh hwloc-bind --cpubind core:80-87 -- ../node-burn/build/burn -ggemm,5000 -d900 & 
pidj22=$!
srun --overlap -n1 ./gpubind1.sh hwloc-bind --cpubind core:88-95 -- ../node-burn/build/burn -ggemm,5000 -d900 & 
pidj23=$!
srun --overlap -n1 ./gpubind1.sh hwloc-bind --cpubind core:96-103 -- ../node-burn/build/burn -ggemm,5000 -d900 & 
pidj24=$!

srun --overlap -n1 ./gpubind2.sh hwloc-bind --cpubind core:144-151 -- ../node-burn/build/burn -ggemm,5000 -d900 & 
pidj31=$!
srun --overlap -n1 ./gpubind2.sh hwloc-bind --cpubind core:152-159 -- ../node-burn/build/burn -ggemm,5000 -d900 & 
pidj32=$!
srun --overlap -n1 ./gpubind2.sh hwloc-bind --cpubind core:160-167 -- ../node-burn/build/burn -ggemm,5000 -d900 & 
pidj33=$!
srun --overlap -n1 ./gpubind2.sh hwloc-bind --cpubind core:168-175 -- ../node-burn/build/burn -ggemm,5000 -d900 & 
pidj34=$!


srun --overlap -n1 ./gpubind3.sh hwloc-bind --cpubind core:216-223 -- ../node-burn/build/burn -ggemm,5000 -d900 & 
pidj41=$!
srun --overlap -n1 ./gpubind3.sh hwloc-bind --cpubind core:224-231 -- ../node-burn/build/burn -ggemm,5000 -d900 & 
pidj42=$!
srun --overlap -n1 ./gpubind3.sh hwloc-bind --cpubind core:232-239 -- ../node-burn/build/burn -ggemm,5000 -d900 & 
pidj43=$!
srun --overlap -n1 ./gpubind3.sh hwloc-bind --cpubind core:240-247 -- ../node-burn/build/burn -ggemm,5000 -d900 & 
pidj44=$!

wait $pidj11 $pidj12 $pidj13 $pidj14 $pidj21 $pidj22 $pidj23 $pidj24 $pidj31 $pidj32 $pidj33 $pidj34 $pidj41 $pidj42 $pidj43 $pidj44

sleep 30
touch stop_monitor
wait $pid

echo quit | nvidia-cuda-mps-control

date
