#!/bin/bash

# Add trap so that "kill" will terminate gracefully 
# It does not seem to work with Slurm
#trap "echo 'Monitoring stopped'; exit 0" SIGTERM

while [ ! -f stop_monitor ];
do
  cat /sys/cray/pm_counters/power >> node_power.txt
  cat /sys/cray/pm_counters/accel0_power >> gpu0_power.txt
  cat /sys/cray/pm_counters/accel1_power >> gpu1_power.txt
  cat /sys/cray/pm_counters/accel2_power >> gpu2_power.txt
  cat /sys/cray/pm_counters/accel3_power >> gpu3_power.txt
  cat /sys/cray/pm_counters/cpu0_power >> cpu0_power.txt
  cat /sys/cray/pm_counters/cpu1_power >> cpu1_power.txt
  cat /sys/cray/pm_counters/cpu2_power >> cpu2_power.txt
  cat /sys/cray/pm_counters/cpu3_power >> cpu3_power.txt
  sleep 5
done
echo "Monitor stopping."
