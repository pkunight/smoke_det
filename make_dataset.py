#coding=utf8

import subprocess
import random
import cv2
import numpy as np

print("unzip data...")
ret = subprocess.run('cd ./data && unzip SmokeDet_DATA_TYY.zip && cd ..', shell=True, check=True, stdout=subprocess.PIPE)

print("make dir...")
ret = subprocess.run('mkdir -p ./data/SmokeDet_DATA_TYY/images/train', shell=True, check=True, stdout=subprocess.PIPE)
ret = subprocess.run('mkdir ./data/SmokeDet_DATA_TYY/images/val', shell=True, check=True, stdout=subprocess.PIPE)

ret = subprocess.run('mkdir -p ./data/SmokeDet_DATA_TYY/labels/train', shell=True, stdout=subprocess.PIPE)
ret = subprocess.run('mkdir ./data/SmokeDet_DATA_TYY/labels/val', shell=True, check=True, stdout=subprocess.PIPE)

print("seperate train dataset and val dataset")
ret = subprocess.run('ls ./data/SmokeDet_DATA_TYY/train_images', shell=True, check=True, stdout=subprocess.PIPE)
train_list = ret.stdout.decode('utf8').strip().split('\n')
random.shuffle(train_list)

# 随机划分80%为训练集, 20%为验证集
sep_index = len(train_list) * 0.8
for index in range(len(train_list)):
    img_file = train_list[index]
    file_head = img_file.split('.')[0]
    label_file = file_head + ".txt"
    dir = "train"
    if index > sep_index:
        dir = "val"
    # 移动图像文件
    command = "mv ./data/SmokeDet_DATA_TYY/train_images/%s ./data/SmokeDet_DATA_TYY/images/%s" % (img_file, dir)
    ret = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE)
    # 移动标签文件
    command = "mv ./data/SmokeDet_DATA_TYY/train_labels/%s ./data/SmokeDet_DATA_TYY/labels/%s" % (label_file, dir)
    ret = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE)

    # 验证集不要翻转图像
    if index > sep_index:
        continue
    # 创建左右翻转的新图像文件
    img = cv2.imread("./data/SmokeDet_DATA_TYY/images/%s/%s" % (dir, img_file))
    img_fliplr = cv2.flip(img, 1)
    cv2.imwrite("./data/SmokeDet_DATA_TYY/images/%s/%s-fliplr.jpg" % (dir, file_head), img_fliplr)
    # 创建左右翻转的新标签文件
    with open("./data/SmokeDet_DATA_TYY/labels/%s/%s" % (dir, label_file), 'r') as read_file:
        with open("./data/SmokeDet_DATA_TYY/labels/%s/%s-fliplr.txt" % (dir, file_head), 'w') as write_file:
            for line in read_file:
                items = line.strip().split(' ')
                if len(items) != 5:
                    continue
                items[1] = str(1.0 - float(items[1]))
                write_file.write(' '.join(items) + '\n')

ret = subprocess.run('rm -rf ./data/SmokeDet_DATA_TYY/train_images', shell=True, stdout=subprocess.PIPE)
ret = subprocess.run('rm -rf ./data/SmokeDet_DATA_TYY/train_labels', shell=True, stdout=subprocess.PIPE)

print("finish")