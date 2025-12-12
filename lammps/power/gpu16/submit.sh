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
srun -u --overlap --ntasks-per-node=1 --output "out-%J.log" hwloc-bind --cpubind core:32-39 -- ./monitor.sh &
sm=$1
sleep 30

srun -u --overlap --ntasks-per-node=1 --output "out-%J.log" ./gpubind0.sh hwloc-bind --cpubind core:0-7 -- lmp -in in.K_500 -log out.K_500_0.log &
j01=$!
srun -u --overlap --ntasks-per-node=1 --output "out-%J.log" ./gpubind0.sh hwloc-bind --cpubind core:8-15 -- lmp -in in.K_600 -log out.K_600_0.log &
j02=$!
srun -u --overlap --ntasks-per-node=1 --output "out-%J.log" ./gpubind0.sh hwloc-bind --cpubind core:16-23 -- lmp -in in.K_750 -log out.K_750_0.log &
j03=$!
srun -u --overlap --ntasks-per-node=1 --output "out-%J.log" ./gpubind0.sh hwloc-bind --cpubind core:24-31 -- lmp -in in.K_1000 -log out.K_1000_0.log &
j04=$!

srun -u --overlap --ntasks-per-node=1 --output "out-%J.log" ./gpubind1.sh hwloc-bind --cpubind core:72-79 -- lmp -in in.K_500 -log out.K_500_1.log &
j11=$!
srun -u --overlap --ntasks-per-node=1 --output "out-%J.log" ./gpubind1.sh hwloc-bind --cpubind core:80-87 -- lmp -in in.K_600 -log out.K_600_1.log &
j12=$!
srun -u --overlap --ntasks-per-node=1 --output "out-%J.log" ./gpubind1.sh hwloc-bind --cpubind core:88-95 -- lmp -in in.K_750 -log out.K_750_1.log &
j13=$!
srun -u --overlap --ntasks-per-node=1 --output "out-%J.log" ./gpubind1.sh hwloc-bind --cpubind core:96-103 -- lmp -in in.K_1000 -log out.K_1000_1.log &
j14=$!

srun -u --overlap --ntasks-per-node=1 --output "out-%J.log" ./gpubind2.sh hwloc-bind --cpubind core:144-151 -- lmp -in in.K_500 -log out.K_500_2.log &
j21=$!
srun -u --overlap --ntasks-per-node=1 --output "out-%J.log" ./gpubind2.sh hwloc-bind --cpubind core:152-159 -- lmp -in in.K_600 -log out.K_600_2.log &
j22=$!
srun -u --overlap --ntasks-per-node=1 --output "out-%J.log" ./gpubind2.sh hwloc-bind --cpubind core:160-167 -- lmp -in in.K_750 -log out.K_750_2.log &
j23=$!
srun -u --overlap --ntasks-per-node=1 --output "out-%J.log" ./gpubind2.sh hwloc-bind --cpubind core:168-175 -- lmp -in in.K_1000 -log out.K_1000_2.log &
j24=$!

srun -u --overlap --ntasks-per-node=1 --output "out-%J.log" ./gpubind3.sh hwloc-bind --cpubind core:216-223 -- lmp -in in.K_500 -log out.K_500_3.log &
j31=$!
srun -u --overlap --ntasks-per-node=1 --output "out-%J.log" ./gpubind3.sh hwloc-bind --cpubind core:224-231 -- lmp -in in.K_600 -log out.K_600_3.log &
j32=$!
srun -u --overlap --ntasks-per-node=1 --output "out-%J.log" ./gpubind3.sh hwloc-bind --cpubind core:232-239 -- lmp -in in.K_750 -log out.K_750_3.log &
j33=$!
srun -u --overlap --ntasks-per-node=1 --output "out-%J.log" ./gpubind3.sh hwloc-bind --cpubind core:240-247 -- lmp -in in.K_1000 -log out.K_1000_3.log &
j34=$!

wait $j01 $j02 $j03 $j04 $j11 $j12 $j13 $j14 $j21 $j22 $j23 $j24 $j31 $j32 $j33 $j34 $j41 $j42 $j43 $j44

sleep 30
touch stop_monitor
wait $sm

echo quit | nvidia-cuda-mps-control
