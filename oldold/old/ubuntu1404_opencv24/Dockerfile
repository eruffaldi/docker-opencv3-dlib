FROM ubuntu:14.04

ENV PYTHON_VERSION 2.7

RUN apt-get -y update

# the following is for add-apt-repository
RUN apt-get install -q -y  software-properties-common usbutils

# this is only for 14.04
RUN add-apt-repository ppa:mc3man/trusty-media

RUN apt-get install -y gstreamer1.0-alsa gstreamer1.0-libav gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-tools x264 libx264-dev libgstreamer1.0-dev

RUN apt-get install -y ffmpeg alsa-base alsa-utils pulseaudio libusb-1.0
RUN apt-get -y install python$PYTHON_VERSION-dev wget unzip libtbb-dev \
                       build-essential cmake git pkg-config libatlas-base-dev gfortran \
                       libjasper-dev libgtk2.0-dev libavcodec-dev libavformat-dev \
                       libswscale-dev libjpeg-dev libpng-dev libtiff-dev libjasper-dev libv4l-dev
RUN wget https://bootstrap.pypa.io/get-pip.py && python get-pip.py
RUN pip install numpy matplotlib

RUN wget https://github.com/opencv/opencv/archive/2.4.13.2.zip -O opencv2.zip && \
    unzip -q opencv2.zip && mv /opencv-2.4.13 /opencv

RUN mkdir /opencv/build
WORKDIR /opencv/build
RUN cmake -D CMAKE_BUILD_TYPE=RELEASE \
	-D CMAKE_CXX_FLAGS=-march=native \
	-D CMAKE_C_FLAGS=-march=native \
	-D ENABLE_AVX2=ON \
	-D ENABLE_AVX=ON \
	-D ENABLE_FMA3=ON \
	-D ENABLE_SSE42=ON \
	-D ENABLE_SSE31=ON \
	-D ENABLE_SSE3=ON \
	-D BUILD_PYTHON_SUPPORT=ON \
	-D BUILD_TESTS=OFF \
	-D BUILD_PERF_TESTS=OFF \
	-D CMAKE_INSTALL_PREFIX=/usr/local \
	-D INSTALL_C_EXAMPLES=OFF \
	-D INSTALL_PYTHON_EXAMPLES=OFF \
	-D BUILD_EXAMPLES=OFF \
	-D BUILD_NEW_PYTHON_SUPPORT=ON \
	-D WITH_IPP=OFF \
	-D WITH_V4L=ON ..
RUN make -j
RUN make install
RUN ldconfig
# Define default command.


# Define default command.
CMD ["bash"]


