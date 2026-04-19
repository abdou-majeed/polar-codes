# decoder.py

import numpy as np
from queue import Queue
from channel_combination import generator
from utils import binarytodec, dectobinary
from transitions import make_UtoY, make_UtoX, make_XtoY
from encoder import coset_encoder, select

# TODO
# MLD BEC
# Successive Cancellation
# add make WN to transitions

def MLD_BSC(n, k, p, encoder):
	# We send all zeros and find the error prob
	N = 2**n
	Q = Queue()
	processed = np.zeros(2**N, dtype=int) # indicates whether an element was already put in the queue
	tie = np.zeros(2**N, dtype=int) # count the number of closest codewords at the same distance from each Y_vec
	tie_weight = np.zeros(2**N, dtype=int) 
	err = 0

	# insert all non-zero codewords in Q
	for U in range(1, 2**k):
		X_vec = encoder(U)
		X = binarytodec(X_vec)
		Q.put((X_vec, 0)) # the Queue contains tuples (vector, d) where d is the distance to the closest codeword)
		processed[X] = 1

	# Dequeue and Enqueue while computing the error prob	
	while not Q.empty():
		Y_vec, d = Q.get()
		w = Y_vec.sum() # weight
		if d == w:
			# Tie: Count the number of codewords at the same distance from Y_vec
			Y = binarytodec(Y_vec)
			if tie_weight[Y] == 0:
				tie_weight[Y] = w
				tie[Y] = 1
			elif w < tie_weight[Y]:
				tie_weight[Y] = w
				tie[Y] = 1
			elif w == tie_weight[Y]:
				tie[Y] += 1
#			err += 0.5 * p**w * (1-p)**(N-w)
		if d < w:
			# DECODED INCORRECTLY: Y_vec is closer to another codeword than to zeros
			err += p**w * (1-p)**(N-w)
		
		if processed.sum() < 2**N: # no need to continue if all y have been processed
			for i in range(N):
				E_vec = np.zeros(N, dtype=int)
				E_vec[i] = 1
				Y_prime_vec = (Y_vec + E_vec) % 2
				Y_prime = binarytodec(Y_prime_vec)
				if processed[Y_prime] == 0:
					Q.put((Y_prime_vec, d+1))
					processed[Y_prime] = 1
	
	counter = 0
	for Y, (count, w) in enumerate(zip(tie, tie_weight)):
		if count > 0:
			counter += 1
			err += (1 - 0.5**count) * p**w * (1-p)**(N-w)
	print("counter:", counter)
	return err

#0.0038955757666264395 0.0038952950367920156
#0.0653510082539884 0.06617612219653103
#0.12034456473921892 0.1328572235372208
#0.1329796944721935 0.17508294614777078
#0.3396357914145873 0.39376902187542373
#0.36369794091597757 0.5031120597392498
#0.41182223991875944 0.5577835786711621
#0.6064472621104556 0.6064397071294122


#0.0038955757666264395 0.0038952950367920156
#0.06535100825398849 0.06617612219653103
#0.12034456473921906 0.1328572235372208
#0.13297969447219346 0.17508294614777078
#0.33963579141458783 0.39376902187542373
#0.36369794091597707 0.5031120597392498
#0.41182223991875766 0.5577835786711621
#0.6064472621104556 0.6064397071294122


#def MLD_BSC(n, k, p, encoder):
#	# We send all zeros and find the error prob
#	N = 2**n
#	Q = Queue()
#	processed = np.zeros(2**N, dtype=int) # indicates whether an element was already put in the queue
#	err = 0
#
#	# insert all non-zero codewords in Q
#	for U in range(1, 2**k):
#		X_vec = encoder(U)
#		X = binarytodec(X_vec)
#		Q.put((X_vec, 0)) # the Queue contains tuples (vector, d) where d is the distance to the closest codeword)
#		processed[X] = 1
#
#	# Dequeue and Enqueue while computing the error prob	
#	while not Q.empty():
#		Y_vec, d = Q.get()
#		w = Y_vec.sum() # weight
#		if d == w:
#			err += 0.5 * p**w * (1-p)**(N-w)			
#		if d < w:
#			# DECODED INCORRECTLY: Y_vec is closer to another codeword than to zeros
#			err += p**w * (1-p)**(N-w)
#		
#		if processed.sum() < 2**N: # no need to continue if all y have been processed
#			for i in range(N):
#				E_vec = np.zeros(N, dtype=int)
#				E_vec[i] = 1
#				Y_prime_vec = (Y_vec + E_vec) % 2
#				Y_prime = binarytodec(Y_prime_vec)
#				if processed[Y_prime] == 0:
#					Q.put((Y_prime_vec, d+1))
#					processed[Y_prime] = 1
#	return err









def select_odd(vec):
	odd_vec = []
	for i in range(0, len(vec), 2):
		odd_vec.append(vec[i])
	return np.array(odd_vec)

def select_even(vec):
	even_vec = []
	for i in range(1, len(vec), 2):
		even_vec.append(vec[i])
	return np.array(even_vec)

def insert(x, dic, keys):
	if len(keys) == 1:
		dic[keys[0]] = x
	elif keys[0] in dic.keys():
		dic[keys[0]] = insert(x, dic[keys[0]], keys[1:])
	else:
		dic[keys[0]] = insert(x, {}, keys[1:])

	return dic







def make_compute_L():
	L_dict = {} # N, i, 0-1

	def compute_L(channel, Y_vec, U_vec):
		W = channel
		N = len(Y_vec)
		i = len(U_vec) + 1
		nonlocal L_dict

		if N == 1:
			if W["trans"][1][Y_vec[0]] == 0:
				return 1
			return W["trans"][0][Y_vec[0]] / W["trans"][1][Y_vec[0]]
		
		if i % 2 == 0:
			j =  int(i/2)
		else:
			j = int((i+1)/2)

		a = L_dict.get(int(N/2), {}).get(j, {}).get(0)
		b = L_dict.get(int(N/2), {}).get(j, {}).get(1)

		if a == None:
			a = compute_L(W, Y_vec[:int(N/2)], (select_odd(U_vec[:2*j-2]) + select_even(U_vec[:2*j-2])) % 2)
			L_dict = insert(a, L_dict, (int(N/2), j, 0))
		if b == None:
			b = compute_L(W, Y_vec[int(N/2):], select_even(U_vec[:2*j-2]))	
			L_dict = insert(b, L_dict, (int(N/2), j, 1))

		if i%2 == 0:
			print("here")
			return a**((1-2*U_vec[2*j-2])) * b
		return (a*b +1)/(a+b)

	return compute_L



def raw_compute_L(channel, Y_vec, U_vec):
	print("U", U_vec)
	W = channel
	N = len(Y_vec)
	i = len(U_vec) + 1

	# print("N:", N)
	if N == 1:
		if W["trans"][1][Y_vec[0]] == 0:
			return 1
		return W["trans"][0][Y_vec[0]] / W["trans"][1][Y_vec[0]]
	
	i += 1 # so j in {1, 2, ...}
	if i % 2 == 0:
		j =  int(i/2)
	else:
		j = int((i+1)/2)

	if 2*(j-1)-2 < 0:
		index = 0
	else:
		index = 2*(j-1)-2
	a = raw_compute_L(W, Y_vec[:int(N/2)], (select_odd(U_vec[:index]) + select_even(U_vec[:index])) % 2)
	b = raw_compute_L(W, Y_vec[int(N/2):], select_even(U_vec[:index]))

	if i%2 == 0:
		# print("tricky")
		if index == 0:
			bit = 1
		else:
			bit = U_vec[index]
		return a**( (1 - 2 * bit)) * b
		# return a**((1-2*U_vec[2*j-2])) * b
	return (a*b +1)/(a+b)


















def make_W_N(n, W):
	UtoY = make_UtoY(n, W)

	def W_N(y, u_minus, u_i):
		N = len(y)
		i = len(u_minus) + 1
		y = int(binarytodec(y))
		prob = 0
		for u_plus in range(2**(N-i)):
			u_plus = dectobinary(u_plus, N-i)
			u = list(u_minus) + [u_i] + u_plus
			u = int(binarytodec(u))

			prob += UtoY(u, y)
		# print(prob)
		return prob

	return W_N

from utils import log
def brute_compute_L(channel, Y_vec, U_vec):
	n = int(log(len(Y_vec)))
	W_N = make_W_N(n, channel)
	a, b = W_N(Y_vec, U_vec, 0), W_N(Y_vec, U_vec, 1)
	if b == 0:
		return 1
	return a / b




def decode_SCD(channel, Y_vec, A, frozen_U = 0):
	W = channel
	N = len(Y_vec)
	U_vec = np.zeros(N, dtype=int)
	frozen_U_vec = np.zeros(N, dtype=int)
	# if frozen_U != 0:
		# 
	# compute_L = make_compute_L()

	for i, bit in enumerate(A):
		if bit == 0:
			U_vec[i] = frozen_U_vec[i]
		else:
			L = scd.compute_L(W, Y_vec, U_vec[:i])
			if L > 1:
				U_vec[i] = 0
			else:
				U_vec[i] = 1
#	print("U_vec", U_vec)
	return U_vec


def SCD(channel, n, A):
	W = channel
	N = 2**n

	encode = coset_encoder(n, A)
	cardA = int(A.sum())
	XtoY = make_XtoY(n, W)

	# We send the all-zeros codeword
	# We loop through Y
	# There is an error when the decoded U is different from zero
	# 

	epsilon = 10**(-6)
	prob = 0
	for Y in range(2**N):
		Y_vec = np.array(dectobinary(Y, N))
		u_vec = np.zeros(N, dtype=int)

		success = True
		nb_of_ties = 0
		for i, bit in enumerate(A):
			if bit == 1:
				L = scd.compute_L(W, Y_vec, u_vec[:i])
				if L < 1 - epsilon:
					## Decode bit as 1
					success = False
					prob += XtoY(0, Y)
					break
				elif 1 - epsilon < L < 1 + epsilon:
					nb_of_ties += 1
		if success and nb_of_ties > 0:
			prob += (1 - 0.5**nb_of_ties) * XtoY(0,Y)

	return prob


	prob = 0
	for Y in range(2**N):
		Y_vec = np.array(dectobinary(Y, N))
		u_vec = decode_SCD(W, Y_vec, A)
		print("Y_vec:", Y_vec, "U_vec", u_vec)
		u_vec_A, _ = select(u_vec, A)
		u_0 = int(binarytodec(u_vec_A))

		x = encode(u_0)
		# print("U", u_vec)
		X = int(binarytodec(x))
		prob += (1/2**cardA) * XtoY(X, Y)

	return 1 - prob








from channels import *
import scd
n = 3
N = 2**n
# A = np.concatenate((np.zeros(int(N/2)), np.array([0]), np.ones(int(N/2)-1)))
# A = np.concatenate((np.ones(int(N/2)), np.zeros(int(N/2))))
A = np.concatenate((np.zeros(int(N/2)), np.ones(int(N/2))))
# print(A)
p = .5
print(SCD(BSC(p), n, A))
# print(MLD_BSC(n, int(N/2), p, encoder=coset_encoder(n, A)))
# print(MLD_BSC(n, int(N/2)-1, .5, encoder=coset_encoder(n, A)))



W = BSC_30
n = 2
N = 2**n
i = 3 # starts at 1

# print("")
# for j in range(10):
# 	Y_vec = np.random.randint(0, 2, size=N)
# 	U_vec = np.random.randint(0, 2, size=i-1)
# 	print("U", U_vec)

# 	compute_L = make_compute_L()
# 	# print("Y:", Y_vec, brute_compute_L(W, Y_vec, U_vec), raw_compute_L(W, Y_vec, U_vec), compute_L(W, Y_vec, U_vec))
# 	# print("Y:", Y_vec, brute_compute_L(W, Y_vec, U_vec), raw_compute_L(W, Y_vec, U_vec))
# 	if( abs(brute_compute_L(W, Y_vec, U_vec) - raw_compute_L(W, Y_vec, U_vec)) > 0.0001) :
# 		print("Y:", Y_vec, "U:", U_vec, brute_compute_L(W, Y_vec, U_vec), raw_compute_L(W, Y_vec, U_vec))
# 	print(U_vec)
# print("")
