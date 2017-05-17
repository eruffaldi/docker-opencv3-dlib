class Dockerfile:
	def __init__(self,origin,body):
		self.origin = origin
		self.body = body
def part_linux(args):
	if args.ubuntu == "14.04":
		return Dockerfile("14.04",
			"""
ENV GCCVERSION=4.9
RUN add-apt-repository ppa:ubuntu-toolchain-r/test
RUN apt-get update
RUN apt-get install -yq g++-$GCCVERSION
RUN update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-$GCCVERSION 50
RUN update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-$GCCVERSION 50
				""")
	elif args.ubuntu == "16.04":
		return Dockerfile("16.04",None)
	else:
		raise "Unknown ubuntu " + args.ubuntu

def part_cudnn(args):
	# download cudnn
	# copy to correct cuda version
	pass

def part_opencv(args):
	prerequisites = """
RUN apt-get install -y ffmpeg alsa-base alsa-utils pulseaudio libusb-1.0
RUN apt-get -y install python$PYTHON_VERSION-dev wget unzip libtbb-dev \
                   build-essential cmake git pkg-config libatlas-base-dev gfortran \
                   libjasper-dev libgtk2.0-dev libavcodec-dev libavformat-dev \
                   libswscale-dev libjpeg-dev libpng-dev libtiff-dev libjasper-dev libv4l-dev
RUN wget https://bootstrap.pypa.io/get-pip.py && python get-pip.py
RUN pip install numpy matplotlib
	"""	
	if args.opencv.startswith("2."):
		fetchpart = """
RUN wget https://github.com/opencv/opencv/archive/2.4.13.2.zip -O ~/opencv2.zip && \
    unzip -q opencv2.zip && mv ~/opencv-2.4.13.2 ~/opencv
		"""
	else:
		fetchpart = """
RUN wget https://github.com/opencv/opencv/archive/3.2.0.zip -O ~/opencv3.zip && \
unzip -q opencv3.zip && mv ~/opencv-3.2.0 ~/opencv
		"""
	return Dockerfile(None,"""
ENV PYTHON_VERSION 2.7

{prerequisites:s}
RUN wget https://bootstrap.pypa.io/get-pip.py && python get-pip.py
RUN pip install numpy matplotlib

{fetchpart:s}

RUN mkdir ~/opencv/build
WORKDIR ~/opencv/build
RUN cmake -D CMAKE_BUILD_TYPE=RELEASE \
	-D CMAKE_CXX_FLAGS=-march=native \
	-D CMAKE_C_FLAGS=-march=native \
	-D ENABLE_AVX2={avx2:s} \
	-D ENABLE_AVX={avx2:s} \
	-D ENABLE_FMA3={avx2:s} \
        -D WITH_TBB=ON \
	-D ENABLE_CUDA={cuda:s} \
	-D ENABLE_SSE42={sse4:s} \
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
	""".format(**dict(prerequisites=prerequisites,fetchpart=fetchpart,sse4="ON" if args.sse4 else "OFF",cuda="ON" if args.cuda != None else "OFF",avx2="ON" if args.avx2 else "OFF")))

def part_dlib(args):
	return Dockerfile(None,"""
RUN apt-get -y install libboost-python-dev
WORKDIR /tmp
RUN wget https://codeload.github.com/davisking/dlib/zip/master -O dlib.zip && \
unzip -q dlib.zip && mv dlib-master dlib
WORKDIR /tmp/dlib
ENV CFLAGS -march=native -O3 -flto 
ENV CXXFLAGS -march=native -O3 -flto
RUN python setup.py {avx2:s} {sse4:s} --yes NDEBUG --yes DLIB_USE_BLAS --yes DLIB_USE_LAPACK build
RUN python setup.py install 
		""".format(**dict(avx2="--yes USE_AVX_INSTRUCTION " if args.avx2 else "",
			sse4="--yes USE_SSE4_INSTRUCTIONS --yes USE_SSE2_INSTRUCTIONS=ON --yes DLIB_HAVE_SSE41 --yes DLIB_HAVE_SSE3 --yes DLIB_HAVE_SSE2" if args.sse4 else "")
		))

def part_ffmpeg(args):
	if args.ubuntu == "14.04":
		return Dockerfile(None,"""
RUN apt-get install -q -y  software-properties-common usbutils
# this is only for 14.04
RUN add-apt-repository ppa:mc3man/trusty-media
RUN apt-get update
RUN apt-get install -y ffmpeg
			""")
	else:
		return Dockerfile(None,"""RUN apt-get install -y ffmpeg
			""")

def part_gstreamer(args):
	if args.gstreamer:
		return Dockerfile(None,"""
RUN apt-get install -y gstreamer1.0-alsa gstreamer1.0-libav gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-tools x264 libx264-dev libgstreamer1.0-dev libgstreamer-plugins-good1.0-dev libgstreamer-plugins-base1.0-dev
""")

def part_boost(args):
	pass


def part_avx2(args):
	pass

def part_sse4(args):
	pass

def part_cuda(args):
	return Dockerfile(None,
"""ARG CUDA_RUN_FILE=cuda_7.5.18_linux.run
ENV PYTHON_VERSION 2.7

ENV CUDA_RUN_FILE ${CUDA_RUN_FILE}

RUN mkdir ~//nvidia
ADD . ~/nvidia/
RUN apt-get update && apt-get install -q -y wget build-essential 

RUN chmod +x ~/nvidia/${CUDA_RUN_FILE}
RUN ~/nvidia/${CUDA_RUN_FILE} --toolkit --silent
RUN rm ~/nvidia/${CUDA_RUN_FILE} 
""")


	pass