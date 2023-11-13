# coding=utf8

# 转换输出:
# 1. ultralytics输出的置信度在最后一位, 但是提交结果要求在第二位
# 2. ultralytics输出的是方框中心点和长宽值, 但是提交结果要求是四条边的坐标

import subprocess

ret = subprocess.run('ls ./runs/detect/predict/labels', shell=True, check=True, stdout=subprocess.PIPE)
label_file_list = ret.stdout.decode('utf8').strip().split('\n')

ret = subprocess.run('mkdir results', shell=True, check=True, stdout=subprocess.PIPE)

for label_file in label_file_list:
    with open("./runs/detect/predict/labels/%s" % (label_file), 'r') as read_file:
        with open("./results/%s" % (label_file), 'w') as write_file:
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
                
                left = center_x - w / 2.0
                right = center_x + w / 2.0
                head = center_y + h / 2.0
                bottom = center_y - h / 2.0
                
                write_file.write("%d %f %f %f %f %f\n" % (label, confidence, left, right, head, bottom))
    
print("finish")