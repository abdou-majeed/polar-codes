# transitions.py

#TODO:
#	monte carlo

import numpy as np
from channel_combination import arikan_generator
from utils import matmul, dectobinary, binarytodec, dectobase


def make_UtoX(n):
	"""Returns a function UtoX that outputs X given U, both decimal integers"""
	# G = generator(n)
	G = arikan_generator(n)
	N = 2**n

	def UtoX(U):
		assert type(U) == int
		assert U < 2**N 
		U_vec = np.array(dectobinary(U, N), dtype=int)
		X_vec = matmul(U_vec, G)
		X = binarytodec(X_vec)
		return int(X) # type numpy.int64
	return UtoX


def raw_make_XtoY(N, channel):
	"""Returns a function XtoY that outputs the probability of Y given X, when sent through N independent copies of the channel"""
	assert type(N) == int and N >= 1
	W = channel
	cardY = len(W["output"])
	
	def XtoY(X, Y):
		assert type(X) == int
		assert X < 2**N
		assert type(Y) == int and Y < cardY**N

		X_bin = dectobinary(X, N)
		Y_digits = dectobase(Y, cardY, N)

		prob = 1
		for x,y in zip(X_bin, Y_digits):
			prob *= W["trans"][x][y]
		return prob

	return XtoY


def make_XtoY(n, channel):
	"""Returns a function XtoY that outputs the probability of Y given X, when sent through N=2**n independent copies of the channel"""
	assert type(n) == int and n >= 0
	N = 2**n
	return raw_make_XtoY(N, channel)


def make_UtoY(n, channel):
	"""Returns a function that outputs the probability of Y given U"""
	assert type(n) == int and n >= 0
	UtoX = make_UtoX(n)
	XtoY = make_XtoY(n, channel)
	
	def UtoY(U, Y):
		return XtoY(UtoX(U), Y)
	return UtoY

