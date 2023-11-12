#coding=utf8

from ultralytics import YOLO

model = YOLO('./runs/detect/train/weights/best.pt')

results = model.predict(source='./data/SmokeDet_DATA_TYY/test_images/',
                      device=0,
                      conf=0.1,
                      save=True,
                      imgsz=640)
