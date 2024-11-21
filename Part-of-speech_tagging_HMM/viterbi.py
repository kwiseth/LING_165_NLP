"""Viterbi algorithm for LING165"""

__author__ = """Hahn Koo (hahn.koo@sjsu.edu)"""

import sys
import math

entry = '<s>'
exit = '</s>'
unk = '<UNK>'
inf = 1e+10000

def neg_log_prob(prob):
	"""Negated log probability"""
	if prob == 0.0: return -inf
	else: return -math.log(prob)

class node:
	"""Trellis node"""
	def __init__(self, label, emitting):
		"""Initializes node.

		Args:
		- label: name of the state represented
		- emitting: whether this represents an emitting state or not
		"""
		self.label = label
		self.emitting = emitting 
		self.delta = 0.0
		self.crumb = None

	def update(self, pc, a, b, obs): 
		"""Updates delta and bread-crumb.

		Args:
		- pc: nodes previous column in the trellis, pc[x] = node labeled x
		- a: transition probabilities, a[x][y] = p(y|x) or p(x->y)
		- b: emission probabilities, b[x][y] = p(y|x) or p(y in x)
		- obs: current observation
		"""
		min_lp = inf
		min_prev = None
		for x in pc.keys():
			tp = a[x].get(self.label,a[x][unk])
			tlp = neg_log_prob(tp)
			lp = pc[x].delta+tlp
			if lp < min_lp:
				min_lp = lp
				min_prev = x
		self.delta = min_lp
		self.crumb = min_prev
		if self.emitting:
			ep = b[self.label].get(obs,b[self.label][unk])
			elp = neg_log_prob(ep)
			self.delta += elp

class trellis:
	"""Trellis"""
	def __init__(self, a, b, obs):
		"""Initializes trellis.

		Args:
		- a: transition probabilities, a[x][y] = p(y|x) or p(x->y)
		- b: emission probabilities, b[x][y] = p(y|x) or p(y in x)
		- obs: a list of observation symbols
		"""
		n = len(obs)
		self.t = {} # t[t][x] = node labeled x in time t
		self.t[0] = {}
		self.t[0][entry] = node(entry,False)
		for i in range(1,n+1):
			self.t[i] = {}
			hit = False # whether there is a state known to emit obs[i-1]
			for state in b.keys():
				if obs[i-1] in b[state]:
					self.t[i][state] = node(state,True)
					hit = True
			if not hit:
				for state in b.keys(): self.t[i][state] = node(state,True)
		self.t[n+1] = {}
		self.t[n+1][exit] = node(exit,False)

	def update(self, a, b, obs):
		"""Updates deltas and bread-crumbs.

		Args:
		- a: transition probabilities, a[x][y] = p(y|x) or p(x->y)
		- b: emission probabilities, b[x][y] = p(y|x) or p(y in x)
		- obs: a list of observation symbols
		"""
		n = len(obs)
		for i in range(1,n+1):
			for x in self.t[i].keys():
				self.t[i][x].update(self.t[i-1],a,b,obs[i-1])
		self.t[n+1][exit].update(self.t[n],a,b,None)

	def backtrace(self):
		"""Follows the crumbs to backtrace.

		Returns:
		- Most likely sequence of states
		"""
		n = len(self.t.keys())
		i = n-1
		cl = [exit]
		while i > 0:
			prev_best = self.t[i][cl[-1]].crumb
			cl.append(prev_best)
			i -= 1
		cl.reverse()
		return cl

	def display(self, a, b, obs):
		"""Display the contents of the trellis."""
		n = len(self.t.keys())
		for i in range(n):
			for x in self.t[i].keys():
				out = '\n'
				out += '# time = '+str(i)
				if i > 0 and i < n-1: out += ', obs = '+obs[i-1]
				out += '\n'
				out += 'node = '+x+'\n'
				out +='delta = '+str(self.t[i][x].delta)+'\n'
				out += 'crumb = '+str(self.t[i][x].crumb)+'\n'
				if i > 0 and i < n-1:
					nod = self.t[i][x]
					ep = b[nod.label].get(obs[i-1],b[nod.label][unk])
					out += 'ep = '+str(ep)+'\n'
					if ep != 0.0:
						print(out)
