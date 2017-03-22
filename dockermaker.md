

We would like to generate dockerfile for different options and configurations ... let's keep it simple

base: ubuntu 14.04 / 16.04 or another if you like
gstreamer
ffmpeg: with caveat for 14.04
optimization: sse4 avx2
cuda:
opencv: 2.x 3.x
	opencvoption: cuda (requires cuda)
dlib: requires opencv3

Can we do it using templates? e.g. requires / provides + macro or just python

pelars requires: opencv 2.x with cuda, ffmpeg

