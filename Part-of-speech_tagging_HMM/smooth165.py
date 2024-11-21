"""Functions for smoothing HMM probabilities"""

__author__ = """Hahn Koo (hahn.koo@sjsu.edu)"""

import time
import sys
import pickle
import sgt

unk = '<UNK>'

def count_types(fd):
	"""Count types. 

	Args:
	- fd[(x,y)] = MLE frequency of (x,y)
	Returns:
	- number of x types
	- number of y types
	"""
	(xl,yl) = ([],[])
	for (x,y) in fd:
		if not x in xl: xl.append(x)
		if not y in yl: yl.append(y)
	v_x = len(xl) 
	v_y = len(yl)
	return (v_x,v_y)

def marginalize(d):
	"""Calculate sum(d[x,y]) over all y with the same x

	Args:
	- d[(x,y)] = some value of (x,y) 
	Returns:
	- md[x] = sum of value of (x,y) over all y with the same x
	"""
	xd = {}
	for key in d:
		if len(key) == 2:
			(x,y) = key
			if not x in xd: xd[x] = {}
			xd[x][y] = d[x,y]
	md = {}
	for x in xd: md[x] = sum(xd[x].values())
	return md

def gt_joint(fd, vx, vy):
	"""Smooth frequencies using GT and compute joint probabilities. 

	Args:
	- fd[(x,y)] = MLE frequency of (x,y)
	- vx: number of possible x types
	- vy: number of possible y types
	Returns:
	- jd[(x,y)] = p_gt(x,y) 
	"""
	nt = sum(fd.values())
	n_xy = len(fd)
	n_0 = (vx*vy)-n_xy
	sfd = sgt.gt_freq(fd)
	jd = {}
	for key in sfd:
		if key == unk: jd[key] = sfd[unk]/n_0
		else: jd[key] = sfd[key]/nt
	return jd
	
def gt_cond(fd, vx, vy):
	"""Smooth frequencies using GT and compute conditional probabilities. 

	Args:
	- fd[(x,y)] = MLE frequency of (x,y)
	- vx: number of possible x types
	- vy: number of possible y types
	Returns:
	- cd[x][y] = p_gt(y|x) 
	"""
	jd = gt_joint(fd,vx,vy)
	md = marginalize(jd)
	cd = {}
	for key in jd:
		if key == unk:
			for x in md:
				if not x in cd: cd[x] = {}
				cd[x][unk] = jd[unk]
		else:
			(x,y) = key
			if not x in cd: cd[x] = {}
			cd[x][y] = jd[key]
	for x in cd:
		denom = sum(cd[x].values())
		n_0 = vy-(len(cd[x])-1)
		denom += jd[unk]*n_0
		for y in cd[x]: cd[x][y] /= denom
	return cd

def lab2(fd):
	"""Shortcut function for LING165-Lab2.

	Args:
	- fd[(x,y)] = MLE frequency of (x,y)
	Returns:
	- cd[x][y] = p_gt(y|x) 
	"""
	(vx,vy) = count_types(fd)
	return gt_cond(fd,vx,vy)

def main(argv):
	(af,bf) = argv
	f = open(af)
	afd = pickle.load(f)
	f.close()
	f = open(bf)
	bfd = pickle.load(f)
	f.close()
	st = time.time()
	(avx,avy) = count_types(afd)
	a = gt_cond(afd,avx,avy)
	et = time.time()
	print '## A complete in',et-st,'seconds.'
	st = time.time()
	(bvx,bvy) = count_types(bfd)
	b = gt_cond(bfd,bvx,bvy)
	et = time.time()
	print '## B complete in',et-st,'seconds.'
	f = open('a','wb')
	pickle.dump(a,f)
	f.close()
	f = open('b','wb')
	pickle.dump(b,f)
	f.close()

if __name__ == '__main__': main(sys.argv[1:]) 
