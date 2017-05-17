TODO
- update at the beginning
- install build essentials
- remove ffmpeg from opencv
- add comment separators
- fix bool flags
- duplicate pip?
- add matplotlib for dlib
- add libfreenect2

# docker-opencv3-dlib
Yet another opencv3 dlib repository. Optimized for SSE/AVX2

Using the makedockers different configurations are possible

## Ubuntu 16.04 + OpenCV 2.x + CUDA + AVX2
python makedockers.py --shell --ubuntu 16.04 --opencv 2.4 --sse4 1 --avx2 1 --gstreamer 1 --ffmpeg 1 --cuda 7.5 --name opencv2cuda_1604

## Ubuntu 16.04 + OpenCV 3.x + AVX2
python makedockers.py --shell --ubuntu 16.04 --opencv 3.2 --sse4 1 --avx2 1 --gstreamer 1 --ffmpeg 1 --name opencv3_1604