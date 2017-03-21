FROM ubuntu1404cuda

ENV PYTHON_VERSION 2.7

RUN wget https://bootstrap.pypa.io/get-pip.py && python get-pip.py
RUN pip install numpy matplotlib

RUN wget https://github.com/opencv/opencv/archive/2.4.13.2.zip -O opencv2.zip && \
    unzip -q opencv2.zip && mv opencv-2.4.13.2 /opencv

RUN apt-get install libtbb-dev

RUN mkdir /opencv/build
WORKDIR /opencv/build
RUN cmake -D CMAKE_BUILD_TYPE=RELEASE \
	-D CMAKE_CXX_FLAGS=-march=native \
	-D CMAKE_C_FLAGS=-march=native \
	-D ENABLE_AVX2=ON \
	-D ENABLE_AVX=ON \
	-D ENABLE_FMA3=ON \
        -D WITH_TBB=ON \
	-D ENABLE_CUDA=ON \
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
ENV CFLAGS -march=native -O3 -flto
ENV CXXFLAGS -march=native -O3 -flto
#RUN python setup.py --yes USE_AVX_INSTRUCTION --yes USE_SSE4_INSTRUCTIONS --yes USE_SSE2_INSTRUCTIONS=ON --yes NDEBUG --yes DLIB_HAVE_SSE41 --yes DLIB_HAVE_SSE3 --yes DLIB_HAVE_SSE2 --yes DLIB_USE_BLAS --yes DLIB_USE_LAPACK build
#RUN python setup.py install 

# Define default command.
CMD ["bash"]


