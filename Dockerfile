FROM nvidia/cuda:11.1.1-runtime-ubuntu18.04

# Copy local file
RUN mkdir /app
WORKDIR /app
COPY . /app
ENV CUDA_LAUNCH_BLOCKING=1

# Update system
RUN apt update
RUN apt upgrade -y
# Install python 3.8
RUN DEBIAN_FRONTEND="noninteractive" apt install -y software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa
RUN DEBIAN_FRONTEND="noninteractive" apt install -y python3.8 python3-pip python3-opencv

# Install python tools
RUN python3.8 -m pip install --upgrade setuptools pip distlib

# Install requirements
RUN python3.8 -m pip install -r requirements.txt



# Test command to check if the GPU is detected 
ENTRYPOINT ["python3.8", "train.py", "--img", "1280", "--batch", "32", "--epochs", "300", "--data", "signatures.yaml", "--weights", "yolov5l.pt", "--device", "0"]
