FROM ubuntu:14.04

ENV PYTHON_VERSION 2.7

ENV CUDA_RUN_FILE cuda_7.5.18_linux.run

RUN mkdir /nvidia
ADD . /nvidia/
RUN apt-get update && apt-get install -q -y wget build-essential 

RUN chmod +x /nvidia/${CUDA_RUN_FILE}
RUN /nvidia/${CUDA_RUN_FILE} --toolkit --silent
RUN rm /nvidia/${CUDA_RUN_FILE} 


RUN apt-get -y update

# the following is for add-apt-repository
RUN apt-get install -y software-properties-common usbutils

RUN apt-get install -y gstreamer1.0-alsa gstreamer1.0-libav gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-tools x264 libx264-dev
RUN add-apt-repository ppa:mc3man/trusty-media
RUN apt-get -y update
RUN apt-get install -y ffmpeg alsa-base alsa-utils pulseaudio libusb-1.0
RUN apt-get -y install python$PYTHON_VERSION-dev wget unzip libtbb-dev \
                       build-essential cmake git pkg-config libatlas-base-dev gfortran \
                       libjasper-dev libgtk2.0-dev libavcodec-dev libavformat-dev \
                       libswscale-dev libjpeg-dev libpng-dev libtiff-dev libjasper-dev libv4l-dev



