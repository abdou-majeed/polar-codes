# encoder.py

# TODO:
# 	move indextoindicator to utils?

import numpy as np
from channel_combination import arikan_generator
from utils import matmul, dectobinary


def select(array, indicator):
	# assertions ?
	shape =  list(array.shape)
	N 	  =  shape[0]
	cardA =  int(np.array(indicator).sum()) # why int? instead of np.int?
	cardB =  N - cardA

	shape[0] = cardA
	shape_A = tuple(shape)
	A = np.zeros(shape_A, dtype=array.dtype)

	shape[0] = cardB
	shape_B = tuple(shape)
	B = np.zeros(shape_B, dtype=array.dtype)

	a, b = 0, 0
	for i, bit in enumerate(indicator):
		if bit:
			A[a] = array[i]
			a += 1
		else:
			B[b] = array[i]
			b += 1
	return A, B


def indextoindicator(n, indices):
	N = 2**n
	indicator = np.zeros(N, dtype=int)
	for index in indices:
		assert index > 0
		indicator[index-1] = 1
	return indicator


def coset_encoder(n, A, frozen_U=0):
	N = 2**n
	G = arikan_generator(n)
	G_A, G_B = select(G, A)
	cardA = int(np.array(A).sum())
	# print(G_A)
	
	# print(cardA)
	if cardA == N:
		frozen_U_vec = np.array([])
	else:
		frozen_U_vec = np.array(dectobinary(frozen_U, N-cardA), dtype=int)
	# print("frozen_U", frozen_U_vec, "G_B", G_B)
	frozen_X_vec = matmul(frozen_U_vec, G_B)
	# print("U_frozen", frozen_U_vec)
	# print("X_frozen", frozen_X_vec)

	def encode(U):
		U_vec = np.array(dectobinary(U, cardA), dtype=int)
		# print("size=", len(U_vec), "U", U, "U_vec", U_vec)

		return (matmul(U_vec, G_A) + frozen_X_vec) % 2
	
	return encode

