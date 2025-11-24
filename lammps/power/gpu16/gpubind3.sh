#!/bin/bash

export CUDA_VISIBLE_DEVICES=3
hwloc-bind --taskset --get

ps -ef | grep mps

"$@"
