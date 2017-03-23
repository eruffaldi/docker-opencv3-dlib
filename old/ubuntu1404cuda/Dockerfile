FROM ubuntu:14.04

ARG CUDA_RUN_FILE=cuda_7.5.18_linux.run
ENV PYTHON_VERSION 2.7

ENV CUDA_RUN_FILE ${CUDA_RUN_FILE}

RUN mkdir /nvidia
ADD . /nvidia/
RUN apt-get update && apt-get install -q -y wget build-essential 

RUN chmod +x /nvidia/${CUDA_RUN_FILE}
RUN /nvidia/${CUDA_RUN_FILE} --toolkit --silent
RUN rm /nvidia/${CUDA_RUN_FILE} 

