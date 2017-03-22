import argparse
from toposort import toposort, toposort_flatten

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
				p.add_parent(self.dparts[q])
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
	pass

def part_dlib(args):
	pass

def part_ffmpeg(args):
	if args.ubuntu == "14.04":
		b = []
	else:
		b = []

def part_gstreamer(args):
	pass

def part_boost(args):
	pass

def part_gcc(args):
	pass

def part_avx2(args):
	pass

def part_sse4(args):
	pass

def part_cuda(args):
	pass

def main():
	parser = argparse.ArgumentParser(description='Builds Dockerfiles')
	parser.add_argument('--opencv',help="opencv version: 2 or 3")
	parser.add_argument('--ubuntu',help="ubuntu version: 14.04 16.04",default="16.04")
	parser.add_argument('--cuda',help="cuda version: 7.5")
	parser.add_argument('--sse4',help="enable sse4",type=bool)
	parser.add_argument('--avx2',help="enable avx2",type=bool)
	parser.add_argument('--dlib',help="enable dlib",type=bool)
	parser.add_argument('--gcc',help="enable gcc update")
	parser.add_argument('--boost',help="enable boost update with this version")
	parser.add_argument('--ffmpeg',help="enable ffmpeg",type=bool,default=True)
	parser.add_argument('--gstreamer',help="enable gstreamer",type=bool,default=True)
	parser.add_argument('--split',help="split docker files",type=bool,default=True)
	parser.add_argument('--name',help="name of output")
	parser.add_argument('--output-dir',help="build dir",default="build")

	args = parser.parse_args()

	parts = Parts()
	parts.add("ubuntu",part_linux,dict(ubuntu="*"),requires=dict())
	parts.add("sse4",part_sse4,dict(ubuntu="*"),requires=dict(),virtual=True)
	parts.add("avx2",part_avx2,dict(ubuntu="*"),requires=dict(),virtual=True)
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
		pass




if __name__ == '__main__':
	main()