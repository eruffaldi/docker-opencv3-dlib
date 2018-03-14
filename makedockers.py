#!/usr/bin/env python
import argparse
from toposort import toposort, toposort_flatten
import os
from definitions import *

#http://stackoverflow.com/questions/15008758/parsing-boolean-values-with-argparse
rdock2shell="""

alias ARG=echo

function RUN()
{
$*
}
function ENV()
{
export $1=$2;
}
function WORKDIR()
{
cd $1;
}
function CMD()
{
echo "CMD $*"
}
function FROM()
{
echo "CMD $*"
}

"""

def docker2shell(x):
	#https://gist.github.com/eruffaldi/7d02d6ec040b9c0498b1e07898b3c827
	#TODO ARG replacement
	q = ["#!/bin/bash"] + rdock2shell.split("\n")
	args = dict()
	for line in x.split("\n"):
		if line.startswith("ARG "):
			name,value = line[4:].split("=",2)
			args[name] = value.strip()
		else:
			if line.find("${") >= 0:
				for k,v in args.items():
					line = line.replace("${%s}" % k,v)
			q.append(line)
	return "\n".join(q)

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


def main():
	parser = argparse.ArgumentParser(description='Builds Dockerfiles')
	parser.add_argument('--opencv',help="opencv version: 2 or (3.2,3.3,3.4 or 3 for last)")
	parser.add_argument('--ubuntu',help="ubuntu version: 14.04 16.04",default="16.04")
	parser.add_argument('--cuda',help="cuda version: 7.5 or 8.0 or 9.0",default="")
	parser.add_argument('--cudaptx',help="cuda compute capabilities: GTX 1080=6.1 GTX960=5.2 GTX770=3.5 K20m=3.5",nargs="+",default=["6.1","5.2","3.5"])
	parser.add_argument('--sse4',help="enable sse4",type=bool,default=True)
	parser.add_argument('--avx2',help="enable avx2",type=bool,default=True)
	parser.add_argument('--pytorch',help="enable pytorch",type=bool,default=True)
	parser.add_argument('--dlib',help="enable dlib",type=bool)
	parser.add_argument('--tensorflow',type=bool,help="installs 1.6")
	parser.add_argument('--cudnn',help="cuddn has to be provided externally")
	parser.add_argument('--python',help="python version",default="2.7")

	#parser.add_argument('--gcc',help="enable gcc update")
	parser.add_argument('--boost',help="enable boost update with this version")
	parser.add_argument('--ffmpeg',help="enable ffmpeg",type=bool,default=True)
	parser.add_argument('--gstreamer',help="enable gstreamer",type=bool,default=True)
	parser.add_argument('--split',help="split docker files",type=bool,default=False)
	parser.add_argument('--name',help="name of output",required=True)
	parser.add_argument('--output-dir',help="build dir for split",default="build")
	parser.add_argument('--shell',help="generate for shell",action="store_true")

	args = parser.parse_args()

	parts = Parts()
	parts.add("ubuntu",part_linux,dict(ubuntu="*"),requires=dict())
	parts.add("sse4",part_sse4,dict(sse4="*"),requires=dict(),virtual=True)
	parts.add("avx2",part_avx2,dict(avx2="*"),requires=dict(),virtual=True)
	parts.add("opencv",part_opencv,dict(opencv="*"),requires=dict(cuda="*",sse4="*",avx2="*",ubuntu="*",ffmpeg="*",gstreamer="*"))
	parts.add("ffmpeg",part_ffmpeg,dict(ffmpeg="*"),requires=dict(ubuntu="*"))
	parts.add("gstreamer",part_gstreamer,dict(gstreamer="*"),requires=dict(ubuntu="*"))
	parts.add("dlib",part_dlib,dict(dlib="*"),requires=dict(opencv="3"))
	parts.add("pytorch",part_pytorch,dict(dlib="*"),requires=dict(opencv="3"))
	parts.add("cuda",part_cuda,dict(cuda="*"),requires=dict(ubuntu="*"))
	parts.add("boost",part_boost,dict(boost="*"),requires=dict(ubuntu="*"))
	#parts.add("gcc",part_gcc,dict(gcc="*"),requires=dict(ubuntu="*"))
	parts.add("cudnn",part_cudnn,dict(cudnn="*"),requires=dict(cuda="*"))
	parts.add("cafe",part_cafe,dict(cafe="*"),requires=dict(cuda="9.0",opencv="*"))
	parts.add("tensorflow",part_tensorflow,dict(tensorflow="*"),requires=dict(cuda="9.0",cudnn="*"))

	# now filter the graph by the conditions of the args, one node at time
	parts.filter(args)

	dd = [p.fx(args) for p in parts.oparts]

	# emit as single, or as parts
	if args.split:
		print "not implemented"
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
					allout.append("FROM %s" % d.origin)
				else:
					raise "Error double origin",d.origin
			if d.body is not None:
				allout.append(d.body)
		if withfrom is None:
			print "some part should specify a source!"
		else:
			if args.shell:
				print "making shell"
				j = args.output_dir
				if not os.path.isdir(j):
					os.makedirs(j)
				open(os.path.join(j,args.name+".sh"),"wb").write(docker2shell("\n".join(allout)))
			else:
				j = os.path.join(args.output_dir,args.name)
				if not os.path.isdir(j):
					os.makedirs(j)
				open(os.path.join(j,"Dockerfile"),"wb").write("\n".join(allout))






if __name__ == '__main__':
	main()