#!/bin/bash
cd preprocessing || return $?
# train.record
python xml_to_record.py -x ~/Tensorflow/workspace/CaptchaBreaker/images/train -l ~/Tensorflow/workspace/CaptchaBreaker/annotations/label_map.pbtxt -o ~/Tensorflow/workspace/CaptchaBreaker/annotations/train.record -i ~/Tensorflow/workspace/CaptchaBreaker/images/train -c ~/Tensorflow/workspace/CaptchaBreaker/annotations/train_labels.csv
# test.record
python xml_to_record.py -x ~/Tensorflow/workspace/CaptchaBreaker/images/test -l ~/Tensorflow/workspace/CaptchaBreaker/annotations/label_map.pbtxt -o ~/Tensorflow/workspace/CaptchaBreaker/annotations/test.record -i ~/Tensorflow/workspace/CaptchaBreaker/images/test -c ~/Tensorflow/workspace/CaptchaBreaker/annotations/test_labels.csv
read -rsn1 -p"Press any key to continue..."; echo
