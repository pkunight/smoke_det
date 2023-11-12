# coding=utf8

# ultralytics输出的置信度在最后一位, 但是提交结果要求在第二位, 因此做一次转换

import subprocess

ret = subprocess.run('ls ./runs/detect/predict4/labels', shell=True, check=True, stdout=subprocess.PIPE)
label_file_list = ret.stdout.decode('utf8').strip().split('\n')

ret = subprocess.run('mkdir results', shell=True, check=True, stdout=subprocess.PIPE)

for label_file in label_file_list:
    with open("./runs/detect/predict4/labels/%s" % (label_file), 'r') as read_file:
        with open("./results/%s" % (label_file), 'w') as write_file:
            for line in read_file:
                items = line.strip().split(' ')
                if len(items) != 6:
                    continue
                tmp = items[5]
                del items[5]
                items.insert(1, tmp)
                write_file.write(' '.join(items) + '\n')
    
print("finish")