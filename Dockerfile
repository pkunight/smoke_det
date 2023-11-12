FROM ubuntu:20.04

RUN apt update \
    && apt install -y python3 python3-pip git unzip \
    && pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118 \
    && pip3 install ultralytics -i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn

RUN mkdir /root/workdir \
    && cd /root/workdir \
    && git clone https://github.com/ultralytics/ultralytics.git

RUN apt update \
    && apt install -y install vim curl \
    && pip3 install opencv-python-headless -i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn

COPY smoke_det.yaml /root/workdir
COPY make_dataset.py /root/workdir
COPY train.py /root/workdir
COPY predict.py /root/workdir
COPY yolov8n.pt /root/workdir