# channel_splitting

import numpy as np
from channel_combination import inverse_generator
from utils import dectobinary, binarytodec, matmul, log

# TODO
# BEC: Z
# BSC: z
# Symmetric: cap and z


def split_BEC(n, epsilon):
	# for n = 0: [0, 1-epsilon]
	# for any n: [0, I(1), I(2), ..., I(N)]
	
	last = [0, 1-epsilon] # for n = 0
	for s in range(1, n+1):
		N = 2**s
		cap = np.zeros(N+1)
		
		for i in range(1, len(last)):
			epsilon = 1 - last[i]
			W1 = 2 * epsilon - epsilon**2
			W2 = epsilon**2
			cap[2*i - 1] 	= 1 - W1
			cap[2*i] 	= 1 - W2
		last = cap

	return cap
	

def split_BEC_all(n, epsilon):
	"""Return split_BEC(j) for all 0 <= j <= n"""
	# for n = 0: [0, 1-epsilon]
	# for any n: [0, I(1), I(2), ..., I(N)]
	
	last = [0, 1-epsilon] # for n = 0
	caps = [last]
	for s in range(1, n+1):
		N = 2**s
		cap = np.zeros(N+1)
		
		for i in range(1, len(last)):
			epsilon = 1 - last[i]
			W1 = 2 * epsilon - epsilon**2
			W2 = epsilon**2
			cap[2*i - 1] 	= 1 - W1
			cap[2*i] 	= 1 - W2
		last = cap
		caps.append(last)

	return caps


def split_BSC(n, p):
	N = 2**n
	G_inv = inverse_generator(n)
	
	def find_capacity(i):
		# N >= i >= 1
	
		joint_distr = np.zeros((2**(i-1), 2)) # W_minus, W_i
		for z in range(2**N):
			if z % (10**6) == 0 and z > 0:
				print("z:", z)
			z_vec = np.array(dectobinary(z, N), dtype=int)
			prob = 1
			for bit in z_vec:
				if bit == 1:
					prob *= p
				else:
					prob *= 1-p
			
			w_vec = matmul(z_vec, G_inv)
			W_minus = binarytodec(w_vec[:i-1])
			W_i = w_vec[i-1]
			joint_distr[W_minus,W_i] += prob

		P = joint_distr
		entropy = 0
		for W_minus in range(2**(i-1)):
			for W_i in (0,1):
				entropy += P[W_minus,W_i] * ( log(P[W_minus].sum()) - log(P[W_minus,W_i]))
		return 1 - entropy
	
	return find_capacity


def split_symmetric(n, channel):
	# TODO
	pass

