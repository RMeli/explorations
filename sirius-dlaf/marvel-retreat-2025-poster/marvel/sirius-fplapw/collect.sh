#!/bin/bash

function collect {
	name=$1
	grep_text=$2
	output=$3

	# Shift first three arguments, already saved
	shift
	shift
	shift

	# Get all remaining arguments
	nodes=("$@")

	for n in "${nodes[@]}"
	do
		fname="${name}/n${n}"
		line=$(grep ${grep_text} ${fname}/slurm-*)
		time=$(echo ${line} | awk '{print $3}')
		units=$(echo ${line} | awk '{print $4}')
		echo "${name},${n},${time},${units}" >> ${output}
	done
}

outfile="results.csv"
echo "library,nodes,time,units" > ${outfile}

n=(0.25)
collect cusolver "^sirius   " ${outfile} "${n[@]}"

n=(0.25 0.5 1 2 4 8)
collect dlaf "^sirius   " ${outfile} "${n[@]}"

n=(0.25 0.5 1 2 8)
collect elpa1 "^sirius   " ${outfile} "${n[@]}"

n=(0.25 0.5 1 2)
collect elpa2 "^sirius   " ${outfile} "${n[@]}"
