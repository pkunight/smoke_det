# Smoke Det 吸烟识别  
  
本代码库包含运行环境的dockerhub链接, 镜像Dockerfile, 相关启动命令说明, 及涉及到的脚本  
  
**DockerHub**  
`docker pull nightwang/ai_model:yolo_gpu`  
  
**目录说明**  
```
/root/  
    workdir/  
        data/  
            Smoke_Det_DATA_TYY.zip  
        runs/
            detect/  
                train  训练模型输出(其中的weight/best.pt是最终用于预测的模型)  
                predict  预测结果输出  
        make_dataset.py  数据预处理  
        smoke_det.yaml  训练数据配置  
        train.py  训练脚本  
        predict.py  预测脚本  
        yolov8n.pt  训练初始化模型结构  
```

### 执行步骤  
#### STEP1 启动和进入docker镜像  
**注意**: 数据没有放到镜像中, 需要提前下载并用-v把.zip文件挂载到/root/workdir/data  
`docker run --name gputest --privileged -itd --net=host --ipc=host --gpus all -v /mnt/data/zhouwang/smoke_det:/root/workdir/data nightwang/ai_model:yolo_gpu`  
  
`docker exec -it gputest bash`  
  
`cd /root/workdir`  
  
#### STEP2 划分和增强数据集  
(1) 划分80%数据作为训练集, 20%数据作为验证集  
(2) 对图像进行左右翻转, 扩充数据集  
`python3 make_dataset.py`  
  
#### STEP3 启动训练  
`python3 train.py`  
  
#### STEP4 执行预测  
**注意**: 需要自行修改加载best.pt模型的路径  
`python3 predict.py`  
  