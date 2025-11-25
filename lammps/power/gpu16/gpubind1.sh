#!/bin/bash

export CUDA_VISIBLE_DEVICES=1
hwloc-bind --taskset --get

ps -ef | grep mps

"$@"
