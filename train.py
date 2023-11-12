#coding=utf8

from ultralytics import YOLO

# 使用yolov8n模型结构从0开始训练
model = YOLO('yolov8n.yaml')

results = model.train(data='./smoke_det.yaml',
                      epochs=1,
                      device=0,
                      pretrained=False,
                      batch=64,
                      cache=True,
                      imgsz=640)
