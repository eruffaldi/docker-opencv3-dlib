class Dockerfile:
	def __init__(self,origin,body):
		self.origin = origin
		self.body = body
def part_linux(args):
	if args.cuda == "":
		base = "ubuntu:" + args.ubuntu
	else:
		bbase = [args.cuda]
		if args.cudnn != "":
			bbase.append("cudnn"+args.cudnn)
		bbase.append("runtime" if args.runtime else "devel")
		bbase.append("ubuntu"+args.ubuntu)
		base = "-".join(bbase)
	if args.ubuntu == "14.04":
		return Dockerfile(base,
			"""
ENV GCCVERSION=4.9
RUN add-apt-repository ppa:ubuntu-toolchain-r/test
RUN apt-get update
RUN apt-get install -yq g++-$GCCVERSION
RUN update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-$GCCVERSION 50
RUN update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-$GCCVERSION 50
				""")
	elif args.ubuntu == "16.04":
		return Dockerfile(base,None)
	else:
		raise "Unknown ubuntu " + args.ubuntu

def part_tensorflow(args):
	return Dockerfile(None,"""
	RUN apt-get install openjdk-8-jdk
	RUN echo "deb [arch=amd64] http://storage.googleapis.com/bazel-apt stable jdk1.8" | sudo tee /etc/apt/sources.list.d/bazel.list
	RUN curl https://bazel.build/bazel-release.pub.gpg | sudo apt-key add -
	RUN apt-get update && sudo apt-get install bazel

	RUN apt-get install python-numpy python-dev python-pip python-wheel
    RUN apt-get install libcupti-dev 
	RUN git clone --depth 1 https://github.com/tensorflow/tensorflow  -b r1.6
	RUN cd tensorflow
	RUN export LD_LIBRARY_PATH=/usr/local/cuda/extra/CUPTI/lib64/
	RUN bazel build --config=opt --config=cuda //tensorflow/tools/pip_package:build_pip_package 
	RUN bazel-bin/tensorflow/tools/pip_package/build_pip_package /tmp/tensorflow_pkg
	RUN pip install /tmp/tensorflow_pkg/tensorflow-*

		""")
def part_cafe(args):
	return Dockerfile(None,"""
		RUN apt-get install libgflags-dev libgoogle-glog-dev liblmdb-dev libprotobuf-dev libleveldb-dev libsnappy-dev libopencv-dev libhdf5-serial-dev protobuf-compiler --no-install-recommends libboost-all-dev libopenblas-dev 
		RUN git clone --depth 1 https://github.com/BVLC/caffe
		RUN caffe && mkdir cmake_build && cd cmake_build
		RUN CFLAGS=-march=native CXXFLAGS=-march=native cmake -DCMAKE_BUILD_TYPE=Release .. 
		RUN make -j
		RUN make install
	""")


def part_pytorch(args):
	cu = "cpu" if args.cuda == "" else args.cuda.replace(".","")
	py = args.python.replace(".","")
	py2 = py + "m"
	version = "0.3.1"
	pip = "pip3" if py.startswith("3") else "pip"
	actions = ["%s install http://download.pytorch.org/whl/%s/torch-%s-cp%s-cp%s-linux_x86_64.whl"%(pip,cu,version,py,py2),"%s install torchvision" % pip]
	return Dockerfile(None,"\n".join(["RUN %s" % x for x in actions]))

def part_opencv(args):
	prerequisites = """
RUN apt-get install -y ffmpeg alsa-base alsa-utils pulseaudio libusb-1.0
RUN apt-get -y install python$PYTHON_VERSION-dev wget unzip libtbb-dev \
                   build-essential cmake git screen pkg-config libatlas-base-dev gfortran \
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
	elif args.opencv.startswith("3.2"):
		fetchpart = """
RUN wget https://github.com/opencv/opencv/archive/3.2.0.zip -O ~/opencv3.zip && \
unzip -q opencv3.zip && mv ~/opencv-3.2.0 ~/opencv
		"""
	elif args.opencv.startswith("3.3"):
		fetchpart = """
RUN wget https://github.com/opencv/opencv/archive/3.3.0.zip -O ~/opencv3.zip && \
unzip -q opencv3.zip && mv ~/opencv-3.3.0 ~/opencv
		"""
	else:
		fetchpart = """
RUN wget https://github.com/opencv/opencv/archive/3.4.1.zip -O ~/opencv3.zip && \
unzip -q opencv3.zip && mv ~/opencv-3.4.1 ~/opencv
		"""
	return Dockerfile(None,"""
ENV PYTHON_VERSION {python:s}

{prerequisites:s}

{fetchpart:s}

RUN mkdir ~/opencv/build
WORKDIR ~/opencv/build
RUN cmake -D CMAKE_BUILD_TYPE=RELEASE \
	-D CMAKE_CXX_FLAGS=-march=native \
	-D CMAKE_C_FLAGS=-march=native \
	-D CUDA_ARCH_BIN={cudaptx:s}\
	-D CUDA_ARCH_PTX={cudaptx:s}\
	-D ENABLE_AVX2={avx2:s} \
	-D ENABLE_AVX={avx2:s} \
	-D ENABLE_FMA3={avx2:s} \
        -D WITH_TBB=ON \
	-D ENABLE_CUDA={cuda:s} \
	-D ENABLE_SSE42={sse4:s} \
	-D ENABLE_SSE31=ON \
	-D ENABLE_SSE3=ON \
	-D WITH_CUBLAS=ON \
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
	""".format(**dict(python=args.python,cudaptx=",".join(args.cudaptx),prerequisites=prerequisites,fetchpart=fetchpart,sse4="ON" if args.sse4 else "OFF",cuda="ON" if args.cuda != "" else "OFF",avx2="ON" if args.avx2 else "OFF")))

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
	pass
def part_cudnn(args):
	pass
#Supported Kernel/Compiler
#CUDA 8.0.61
#	Ubuntu 16.04	4.4.0	5.3.1
#	Ubuntu 14.04	3.13	4.8.2	
#CUDA 7.5.18
#	TBD

# Last Table
# http://docs.nvidia.com/cuda/cuda-installation-guide-linux/#axzz4hOtgcDSj
# Compiler Issues:
# CUDA 7.5 and GCC > 4.9 not supported
#	PATCH
#	$ sudo vim /usr/local/cuda/include/host_config.h
# CUDA 7.0 and GCC > 4.8 not supported
#	$ sudo vim /usr/local/cuda/include/host_config.h
#
# Testing:
#	cd /usr/local/cuda/samples/1_Utilities/deviceQuery
# sudo make
# 	./deviceQuery
#	http://kislayabhi.github.io/Installing_CUDA_with_Ubuntu/
def OLD_part_cuda(args):
	if args.cuda == "7.5":
		pre = """ARG CUDA_RUN_FILE=cuda_7.5.18_linux.run
ARG CUDA_URL=http://developer.download.nvidia.com/compute/cuda/7.5/Prod/local_installers/cuda_7.5.18_linux.run
		"""
	elif args.cuda == "8.0":
		pre = """ARG CUDA_RUN_FILE=cuda_8.0.61_375.26_linux-run
ARG CURA_URL=https://developer.nvidia.com/compute/cuda/8.0/Prod2/local_installers/cuda_8.0.61_375.26_linux-run
		"""
	elif args.cuda == "9.0":
		pre = """ARG CUDA_RUN_FILE=cuda_9.0.176_384.81_linux-run
ARG CURA_URL=https://developer.nvidia.com/compute/cuda/9.0/Prod/local_installers/cuda_9.0.176_384.81_linux-run
		"""
	return Dockerfile(None,
pre+
"""
ENV PYTHON_VERSION {python:s}

ENV CUDA_RUN_FILE ${CUDA_RUN_FILE}
ENV CUDA_URL ${CUDA_URL}

RUN mkdir ~//nvidia
ADD . ~/nvidia/
RUN apt-get update && apt-get install -q -y wget build-essential 

RUN chmod +x ~/nvidia/${CUDA_RUN_FILE}
RUN ~/nvidia/${CUDA_RUN_FILE} --toolkit --silent --override
RUN rm ~/nvidia/${CUDA_RUN_FILE} 
""")


	pass