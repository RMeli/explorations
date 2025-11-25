#!/bin/bash

export CUDA_VISIBLE_DEVICES=0
hwloc-bind --taskset --get

ps -ef | grep mps

"$@"
