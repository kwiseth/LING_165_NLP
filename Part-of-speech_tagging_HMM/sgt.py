"""Simple Good-Turing Smoothing - Gale and Sampson (1995)"""

__author__ = """Hahn Koo (hahn.koo@sjsu.edu)"""

import sys
import math
import rpy

unknown_symbol='<UNK>'

def count_freq(freq_dict):
	"""Count frequencies.

	Args:
		freq_dict[entry] = frequency
	Returns:
		d[freq] = frequency of freq
	"""
	d={}
	for entry in freq_dict.keys():
		freq = freq_dict[entry]
		if not d.has_key(freq): d[freq] = 0
		d[freq] += 1
	return d

def fix_zero(freq_freq_dict):
	"""Fix zero frequencies in freq-freq-dictionary.

	Args:
		freq_freq_dict: frequency of frequencies
	Returns:
		Updated freq-freq-dict
	"""
	# 1. Order freq-freq by frequencies.
	c_list = freq_freq_dict.keys()
	c_list.sort()
	# 2. Append zero at the beginning.
	c_list = [0]+c_list
	# 3. Append 2*j-i at the end.
	max_c = c_list[-1]
	prev_max_c = c_list[-2]
	end_freq = 2*max_c-prev_max_c
	c_list.append(end_freq)
	# 4. Fix freq-freq's.
	# Define buckets, each spanning three consecutive frequencies.
	# The first and the last freq mark the range of freq's that can be in the bucket.
	# Distribute the freq of mid-freq among all freq's that can be in the bucket.
	for i in range(1,len(c_list)-1):
		bucket_first_freq = int(c_list[i-1])
		bucket_last_freq = int(c_list[i+1])
		bucket_val = c_list[i]/(0.5*(bucket_last_freq-bucket_first_freq))
		for freq in range(bucket_first_freq+1,bucket_last_freq):
			freq_freq_dict[freq] = bucket_val
	return freq_freq_dict

def linear_regression(freq_freq_dict):
	"""Find the parameters of the straight line through items of freq_freq_dict via linear regression.

	Args:
		freq_freq_dict[freq] = frequency of frequencies
	"""
	log_c = []
	log_n_c = []
	for c in freq_freq_dict.keys():
		n_c = freq_freq_dict[c]
		log_c.append(math.log(c))
		log_n_c.append(math.log(n_c))
	if len(log_c) == 1: (slope,intercept) = (1.0,0.0)
	else:
		lm = rpy.r.lsfit(log_c,log_n_c)
		slope = lm['coefficients']['X']
		intercept = lm['coefficients']['Intercept']
	return (slope,intercept)

def sc(c, n, slope, intercept):
	"""Estimate E(N_c) by the smoothing function of freq:
	S(c)=a*b^c
	logS(freq)=intercept+slope*log(freq)

	Args:
		c: frequency
		n: frequency of c
		slope,intercept: parameters of linear regression model
	"""
	if c == 0: s_c = n
	else:
		log_s_c = intercept+slope*math.log(c)
		s_c = pow(math.e,log_s_c)
	return s_c

def lgt(c, n, slope, intercept):
	"""Get adjusted frequency:
	c* = (c+1)*(S(c+1)/S(c))

	Args:
	- c: frequency
	- n: frequency of c
	- slope,intercept: parameters of linear regression model
	Returns:
	- c* = (c+1)*S(c+1)/S(c)
	"""
	scale = sc(c+1,n,slope,intercept)/sc(c,n,slope,intercept)
	return (c+1)*scale

def turing(c, c_dict, n):
	"""Turing esitmate of c, i.e. use c_dict[c] as N_c:
	c* = (c+1)*N_c+1/N_c

	Args:
	- c: frequency
	- n: frequency of c
	- c_dict: freq-freq-dict
	Returns:
	- c* = (c+1)*N(c+1)/N(c)
	"""
	if c == 0: freq_star = (c+1)*c_dict[c+1]/n
	else: freq_star = (c+1)*c_dict[c+1]/c_dict[c]
	return freq_star 

def var_turing(c, c_dict):
	"""Variance for the Turing estimate.

	Args:
		c: frequency
		c_dict: freq-freq-dict
	"""
	prod = 1.0
	prod *= pow(c,2)
	prod *= float(c_dict[c+1])/pow(c_dict[c],2)
	prod *= (1+float(c_dict[c+1])/c_dict[c])
	return prod

def freq_star_dict(c_dict, n, slope, intercept):
	"""Create adjusted frequency dictionary.

	Args:
	- c_dict: freq-freq-dict
	- n: frequency of c
	- slope,intercept: parameters of linear regression model
	"""
	c_star_dict = {}
	e_c = 'turing'
	for c in [0]+c_dict.keys():
		if c == 0: c_star = turing(c,c_dict,n)
		else:
			lgt_c = lgt(c,n,slope,intercept)
			if e_c == 'turing':
				t_c = turing(c,c_dict,n)
				diff = lgt_c-t_c
				if diff <= 1.65*var_turing(c,c_dict): e_c = 'lgt'
				else: c_star = t_c
			if e_c == 'lgt': c_star = lgt_c
		c_star_dict[c] = c_star
	return c_star_dict

def gt_freq(freq_dict): 
	"""Get Good-Turing smoothed frequency estimates from freq_dict.
	
	Args:
		freq_dict: raw, unsmoothed frequency dictionary
	"""
	# 1. Get frequency of frequencies.
	n = sum(freq_dict.values())
	c_dict = count_freq(freq_dict)
	c_dict = fix_zero(c_dict)
	# 2. Define smoothing function to get expected frequecy of frequencies.
	(slope,intercept) = linear_regression(c_dict)
	# 3. Get adjusted frequencies.
	c_star_dict = freq_star_dict(c_dict,n,slope,intercept)
	# 4. Update freq_dict with adjusted frequencies.
	gt_freq_dict = {}
	gt_freq_dict[unknown_symbol] = c_star_dict[0]
	for key in freq_dict.keys():
		c = freq_dict[key]
		c_star = c_star_dict[c]
		gt_freq_dict[key] = c_star
	return gt_freq_dict

def main():
	# 1. Load freq_dict.
	lines = sys.stdin.readlines()
	freq_dict = {}
	for line in lines:
		ll = line.rstrip().split('\t')
		item = ll[0]
		count = int(ll[1])
		freq_dict[item] = count
	# 2. Print out GT-smoothed probability for each item in freq_dict.
	gt_dict = gt(freq_dict)
	#for key in gt_dict.keys(): print key,'\t',gt_dict[key]
	print('p(unk)=',gt_dict[unknown_symbol])
	print(sum(gt_dict.values()))

if __name__=='__main__': main()
