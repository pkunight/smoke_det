#coding=utf8

from ultralytics import YOLO

model = YOLO('./runs/detect/train5/weights/best.pt')

results = model.val(iou=0.5)
