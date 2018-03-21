NOTE: now NVIDIA is providing pre-made CUDA/CUDNN images from 16.04 we need to modify this script to use them directly when cuda and cudnn are specified (https://hub.docker.com/r/nvidia/cuda/)


# docker-opencv3-dlib
Yet another opencv3 dlib repository. Optimized for SSE/AVX2

Using the makedockers different configurations are possible

## Ubuntu 16.04 + OpenCV 2.x + CUDA + AVX2
python makedockers.py --shell --ubuntu 16.04 --opencv 2.4 --sse4 1 --avx2 1 --gstreamer 1 --ffmpeg 1 --cuda 7.5 --name opencv2cuda_1604

## Ubuntu 16.04 + OpenCV 3.x + AVX2
python makedockers.py --shell --ubuntu 16.04 --opencv 3.2 --cuda 7.5 --sse4 1 --avx2 1 --gstreamer 1 --ffmpeg 1 --dlib 1 --name opencv3_cuda_dlib_1604
