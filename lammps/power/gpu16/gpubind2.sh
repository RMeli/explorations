#!/bin/bash

export CUDA_VISIBLE_DEVICES=2
hwloc-bind --taskset --get

ps -ef | grep mps

"$@"
