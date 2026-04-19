# channel_combination.py

# TODO:

import numpy as np
from utils import dectobinary


# For the generator of Arikan:
# the z are in decreasing order, odd first
# the leftmost bit of z is the lsb ?
def arikan_generator(n):
	N = 2**n
	G = np.zeros((N,N), dtype=int)
	
	for i in range(N):
		monomial = dectobinary(i, n)
		range_z = [i for i in range(1,N,2)][::-1] + [i for i in range(0,N,2)][::-1]
		for z,j in enumerate(range_z):
		# for j in range(N):
			z = dectobinary(z, n)
			product = 1
			for var, bit in zip(monomial, z):
				if var == 1:
					product *= bit
			G[N-1-i,j] = product # N-1-i because the monomials are in reverse order in the matrix.
	return G



def generator(n):
	N = 2**n
	G = np.zeros((N,N), dtype=int)
	
	for i in range(N):
		monomial = dectobinary(i, n)
		for j in range(N):
			z = dectobinary(j, n)
			product = 1
			for var, bit in zip(monomial, z):
				if var == 1:
					product *= bit
			G[N-1-i,j] = product # N-1-i because the monomials are in reverse order in the matrix.
	return G

def inverse_generator(n):
	N = 2**n
	G_inv = np.zeros((N,N), dtype=int)
	
	for i in range(N):
		monomial = dectobinary(i, n)
		for j in range(N):
			z = dectobinary(j, n)
			product = 1
			for var, bit in zip(monomial, z):
				if var == 0:
					product *= 1 - bit
			G_inv[N-1-i,j] = product # N-1-i because the monomials are in reverse order in the matrix.
	return G_inv	

# from utils import matmul
# print(matmul(generator(3), inverse_generator(3)))
# print( (matmul(generator(7), inverse_generator(7)) == np.eye(2**7)).sum() == 2**14 )

# print(arikan_generator(2))
# print(generator(2))
