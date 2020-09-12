#!/bin/bash
conda activate tensorflow
cd ~/Tensorflow/workspace/CaptchaBreaker/ || return $?
tensorboard --logdir=models/my_ssd_resnet50_v1_fpn & firefox "http://localhost:6006/"
