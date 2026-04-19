# main.py
from utils import *
from channels import *
from transitions import *
from channel_combination import*
from channel_splitting import *
from encoder import *
from decoder import *

import numpy as np
import matplotlib.pyplot as plt

# TODO




def first(l):
	return l[0]

def second(l):
	return l[1]

fig = -1



#### BSC
def test_BSC():
	global fig
	folder = "BSC_11003"
	MAX = 4 # maximum value of n 
	p 	= .11003
	BSC_cap = []
	sorted_BSC = []

	print("\n\n-->BSC(" + str(p) + ")")
	for n in range(MAX+1):
		print("\n\t\tn =", n)
		cap = split_BSC(n, p)
		arr = [0]
		sorted_arr = []
		for i in range(1, 2**n + 1):
			c = cap(i)
			arr.append(c)
			sorted_arr.append((i,c))
			print(i, "\t", c)
		BSC_cap.append(arr)
		sorted_arr.sort(key=second, reverse=True)
		sorted_BSC.append(sorted_arr)
		print("\t", [item[0] for item in sorted_arr])

	# for n in range(MAX+1):
#		fig += 1
#		plt.figure(fig)
#		plt.plot(BSC_cap[n], "b.", label="BSC(" + str(p) + ") ; n=" + str(n))
#		plt.legend()
#		plt.savefig(folder + "/BSC_" + str(n))
#		plt.show()


	print("\n\nMLD error")
	for n, sorted_arr in enumerate(sorted_BSC):
		capacity = .5 ##
		k = int(capacity * 2**n)
		encoder = coset_encoder(n, indextoindicator(n, [first(item) for item in sorted_arr[:k]]))
		print(n, "\t", MLD_BSC(n, k, p, encoder))

	return BSC_cap, sorted_BSC

BSC_cap, sorted_BSC = test_BSC()


#encoder = coset_encoder(3, [0,0,0,1,0,1,1,1])
#print(MLD_BSC(3, 4, .11003, encoder)) 



# why BEC and BSC ordering are different
# find minimum distance for given code that achieves capacity
# what sort of sampling to do to make the algorithm faster? decrease resolution
# use pypy



# choose different capacities 0.1 .2 .3
# same ordering for each even when the capacity changes? BSC? BEC?
# choose the 16 polar codes. take when they are the same, when they are different
# find MLD err prob
# plot as fct of capacity for both and for when they are same/diff
# plot for n=4,5,6 goal

# try n=5
# write c++
# nb of core, parallell, online clusters




#### BEC
def test_BEC():
	global fig
	folder = "BEC_50"
	MAX = 4 # maximum value of n 
	p 	= .5
	BEC_cap = []
	sorted_BEC = []

	print("\n\n-->BEC(" + str(p) + ")")
	BEC_cap = split_BEC_all(MAX, p)

	for n, cap in enumerate(BEC_cap):
		print("\n\t\tn =", n)
		sorted_arr = []
		for i in range(1, 2**n + 1):
			sorted_arr.append((i, cap[i]))
			print(i, "\t", cap[i])
		sorted_arr.sort(key=second, reverse=True)
		sorted_BEC.append(sorted_arr)
		print("\t", [item[0] for item in sorted_arr])

#	for n in range(MAX+1):
#		fig += 1
#		plt.figure(fig)
#		plt.plot(BEC_cap[n], "b.", markersize=2, label="BEC(" + str(p) + ") ; n=" + str(n))
#		plt.legend()
#		plt.savefig(folder + "/BEC_" + str(n))
#		plt.show()

	return BEC_cap, sorted_BEC

BEC_cap, sorted_BEC = test_BEC()


print("\n\n")
for n, (bsc, bec) in enumerate(zip(sorted_BSC, sorted_BEC)):
	print(n, [a[0] == b[0] for a,b in zip(bsc,bec)], [b[1]-a[1] for a,b in zip(bsc,bec)])


# comp = [b-a for a,b in zip(BSC_cap, BEC_cap)]
	
# fig += 1
# plt.figure(fig)
# plt.plot(BSC_cap[4], "b.", markersize=2, label="BSC(" + str(.11003) + ") ; n=" + str(4))
# plt.plot(BEC_cap[4], "r.", markersize=2, label="BEC(" + str(.5) + ") ; n=" + str(4))
# plt.legend()
# plt.savefig("comparaison")
# plt.show()



# fig += 1
# plt.figure(fig)
# plt.plot(comp, "b.", markersize=4, label="BEC - BSC ; I(W) = .5 ; n = 4")
# plt.legend()
# plt.savefig("comparaison_2")
# plt.show()






















#n = 4
#N = 2**n
#order = [16, 15, 14, 12, 8, 13, 11, 7, 10, 6, 4, 9, 5, 3, 2, 1]
#err = np.zeros(N-)
#for i in range(N-1):
#	A = indextoindicator(n, order[:i+1])
#	encoder = coset_encoder(n, A)
#	err[i] = MLD_BSC(n, i+1, .11003, encoder);

#print(err)
#plt.plot(np.arange(1, 16), err, "b.")
#plt.show()


















