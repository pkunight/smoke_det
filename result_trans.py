# coding=utf8

# 转换输出:
# 1. ultralytics输出的置信度在最后一位, 但是提交结果要求在第二位
# 2. ultralytics输出的是方框中心点和长宽值, 但是提交结果要求是四条边的坐标

import subprocess
import cv2

ret = subprocess.run('ls ./runs/detect/predict/labels', shell=True, check=True, stdout=subprocess.PIPE)
label_file_list = ret.stdout.decode('utf8').strip().split('\n')

ret = subprocess.run('ls ./data/SmokeDet_DATA_TYY/test_images', shell=True, check=True, stdout=subprocess.PIPE)
image_file_list = ret.stdout.decode('utf8').strip().split('\n')
image_dict = {}
for image_file in image_file_list:
    image_dict[image_file.split('.')[0]] = image_file

ret = subprocess.run('mkdir results', shell=True, check=True, stdout=subprocess.PIPE)

for label_file in label_file_list:
    with open("./runs/detect/predict/labels/%s" % (label_file), 'r') as read_file:
        with open("./results/%s" % (label_file), 'w') as write_file:
            image_file = image_dict[label_file.split('.')[0]]
            img = cv2.imread("./data/SmokeDet_DATA_TYY/test_images/%s" % (image_file))
            height = img.shape[0]
            width = img.shape[1]
            print("img: %s, width: %d, height: %d" % (image_file, width, height))
            for line in read_file:
                items = line.strip().split(' ')
                if len(items) != 6:
                    continue
                label = int(items[0])
                center_x = float(items[1])
                center_y = float(items[2])
                w = float(items[3])
                h = float(items[4])
                confidence = float(items[5])
                
                left = (center_x - w / 2.0) * width
                right = (center_x + w / 2.0) * width
                top = (center_y + h / 2.0) * height
                bottom = (center_y - h / 2.0) * height
                
                write_file.write("%d %f %f %f %f %f\n" % (label, confidence, left, bottom, right, top))
    
print("finish")