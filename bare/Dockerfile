FROM ubuntu:16.04

ENV PYTHON_VERSION 2.7

RUN apt-get -y update

RUN apt-get install -y gstreamer1.0-alsa gstreamer1.0-libav gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-tools x264 libx264-dev
RUN apt-get install -y ffmpeg alsa-base alsa-utils pulseaudio libusb-1.0
RUN apt-get -y install python$PYTHON_VERSION-dev wget unzip libtbb-dev \
                       build-essential cmake git pkg-config libatlas-base-dev gfortran \
                       libjasper-dev libgtk2.0-dev libavcodec-dev libavformat-dev \
                       libswscale-dev libjpeg-dev libpng-dev libtiff-dev libjasper-dev libv4l-dev
RUN wget https://bootstrap.pypa.io/get-pip.py && python get-pip.py
RUN pip install numpy matplotlib

RUN wget https://github.com/opencv/opencv/archive/3.2.0.zip -O opencv3.zip && \
    unzip -q opencv3.zip && mv /opencv-3.2.0 /opencv

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
	-D WITH_IPP=ON \
	-D WITH_V4L=ON ..
RUN make -j
RUN make install
RUN ldconfig
# Define default command.

# Install DLIB master
RUN apt-get -y install libboost-python-dev
WORKDIR /tmp
RUN wget https://codeload.github.com/davisking/dlib/zip/master -O dlib.zip && \
    unzip -q dlib.zip && mv dlib-master dlib
WORKDIR /tmp/dlib
ENV CFLAGS -march=native -O3 -flto -j
ENV CXXFLAGS -march=native -O3 -flto -j
RUN python setup.py --yes USE_AVX_INSTRUCTION --yes USE_SSE4_INSTRUCTIONS --yes USE_SSE2_INSTRUCTIONS=ON --yes NDEBUG --yes DLIB_HAVE_SSE41 --yes DLIB_HAVE_SSE3 --yes DLIB_HAVE_SSE2 --yes DLIB_USE_BLAS --yes DLIB_USE_LAPACK build
RUN python setup.py install 

# Define default command.
CMD ["bash"]


