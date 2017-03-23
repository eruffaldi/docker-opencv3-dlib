import argparse
from toposort import toposort, toposort_flatten

#http://stackoverflow.com/questions/15008758/parsing-boolean-values-with-argparse

def xtoposort(a):
	q = list(a)
	qi = dict([(p,i) for i,p in enumerate(q)])

	# int -> listint
	r = dict([(i,set({qi[x] for x in v.parents})) for v,i in qi.iteritems()])
	print "input",r
	l = toposort(r)
	rr = []
	for x in list(l):
		rr.extend([q[i] for i in x])
	return rr

class Dockerfile:
	def __init__(self,origin,body):
		self.origin = origin
		self.body = body
class Node:
	def __init__(self,name):
		self.name = name
		self.parents = []
		self.children = []
		self.variants = []
	def add_parent(self,p):
		self.parents.append(p)
		p.children.append(self)
	def __repr__(self):
		return "Node(%s)" % self.name
	def active(self,args):
		for k,v in self.conditions.iteritems():
			if hasattr(args,k):
				w = getattr(args,k)
				if v == "*":
					if w is None or w is False:
						return False
				elif w != v:
					return False
			else:
				return False
		return True


class Parts:
	def __init__(self):
		self.parts = []

	def add(self,name,fx,conditions,requires,virtual=False):
		p = Node(name)
		p.fx = fx
		p.conditions = conditions
		p.virtual = virtual
		p.requires = requires
		self.parts.append(p)
	def filter(self,args):
		self.aparts = [p for p in self.parts if p.active(args)]		
		self.dparts = dict([(p.name,p) for p in self.aparts])
		for p in self.dparts.values():
			for q in p.requires.keys():
				w = self.dparts.get(q)
				if w is not None:
					p.add_parent(w)
		# now build the network and order
		self.oparts = xtoposort(self.dparts.values())
		print self.oparts
def part_linux(args):
	if args.ubuntu == "14.04":
		return Dockerfile("14.04",None)
	elif args.ubuntu == "16.04":
		return Dockerfile("16.04",None)
	else:
		raise "Unknown ubuntu " + args.ubuntu

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
RUN wget https://github.com/opencv/opencv/archive/2.4.13.2.zip -O opencv2.zip && \
    unzip -q opencv2.zip && mv /opencv-2.4.13.2 /opencv
		"""
	else:
		fetchpart = """
RUN wget https://github.com/opencv/opencv/archive/3.2.0.zip -O opencv3.zip && \
unzip -q opencv3.zip && mv /opencv-3.2.0 /opencv
		"""
	return Dockerfile(None,"""
ENV PYTHON_VERSION 2.7

{prerequisites:s}
RUN wget https://bootstrap.pypa.io/get-pip.py && python get-pip.py
RUN pip install numpy matplotlib

{fetchpart:s}

RUN mkdir /opencv/build
WORKDIR /opencv/build
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
RUN apt-get install -y gstreamer1.0-alsa gstreamer1.0-libav gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-tools x264 libx264-dev libgstreamer1.0-dev
""")

def part_boost(args):
	pass

def part_gcc(args):
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

RUN mkdir /nvidia
ADD . /nvidia/
RUN apt-get update && apt-get install -q -y wget build-essential 

RUN chmod +x /nvidia/${CUDA_RUN_FILE}
RUN /nvidia/${CUDA_RUN_FILE} --toolkit --silent
RUN rm /nvidia/${CUDA_RUN_FILE} 
""")


	pass

def main():
	parser = argparse.ArgumentParser(description='Builds Dockerfiles')
	parser.add_argument('--opencv',help="opencv version: 2 or 3")
	parser.add_argument('--ubuntu',help="ubuntu version: 14.04 16.04",default="16.04")
	parser.add_argument('--cuda',help="cuda version: 7.5",default="")
	parser.add_argument('--sse4',help="enable sse4",type=bool,default=True)
	parser.add_argument('--avx2',help="enable avx2",type=bool,default=True)
	parser.add_argument('--dlib',help="enable dlib",type=bool)
	parser.add_argument('--gcc',help="enable gcc update")
	parser.add_argument('--boost',help="enable boost update with this version")
	parser.add_argument('--ffmpeg',help="enable ffmpeg",type=bool,default=True)
	parser.add_argument('--gstreamer',help="enable gstreamer",type=bool,default=True)
	parser.add_argument('--split',help="split docker files",type=bool,default=False)
	parser.add_argument('--name',help="name of output")
	parser.add_argument('--output-dir',help="build dir",default="build")

	args = parser.parse_args()

	parts = Parts()
	parts.add("ubuntu",part_linux,dict(ubuntu="*"),requires=dict())
	parts.add("sse4",part_sse4,dict(sse4="*"),requires=dict(),virtual=True)
	parts.add("avx2",part_avx2,dict(avx2="*"),requires=dict(),virtual=True)
	parts.add("opencv",part_opencv,dict(opencv="*"),requires=dict(cuda="*",sse4="*",avx2="*",ubuntu="*",ffmpeg="*",gstreamer="*"))
	parts.add("ffmpeg",part_ffmpeg,dict(ffmpeg="*"),requires=dict(ubuntu="*"))
	parts.add("gstreamer",part_gstreamer,dict(gstreamer="*"),requires=dict(ubuntu="*"))
	parts.add("dlib",part_dlib,dict(dlib="*"),requires=dict(opencv="3"))
	parts.add("cuda",part_cuda,dict(cuda="*"),requires=dict(ubuntu="*"))
	parts.add("boost",part_boost,dict(boost="*"),requires=dict(ubuntu="*"))
	parts.add("gcc",part_gcc,dict(gcc="*"),requires=dict(ubuntu="*"))

	# now filter the graph by the conditions of the args, one node at time
	parts.filter(args)

	dd = [p.fx(args) for p in parts.oparts]

	# emit as single, or as parts
	if args.split:
		pass
	else:
		allout = []
		withfrom = None
		print dd
		for d in dd:
			if d is None:
				continue
			if d.origin is not None:
				if withfrom is None:
					withfrom = d.origin
					allout.append("FRAME %s" % d.origin)
				else:
					raise "Error double origin",d.origin
			if d.body is not None:
				allout.append(d.body)
		if withfrom is None:
			print "some part should specify a source!"
		else:
			open("out.docker","wb").write("\n".join(allout))






if __name__ == '__main__':
	main()