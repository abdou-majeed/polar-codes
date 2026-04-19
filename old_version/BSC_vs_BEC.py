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

# choose capacity
# choose n
# compute BSC cap
# compute BEC cap
# plot each separately
# plot both on same graph
# plot difference
# sort each
# find difference in order and write to file
# record everything else ?


def first(l):
	return l[0]

def second(l):
	return l[1]


MAX_n = 4
# MAX_n = 3
CAPACITIES = (10, 20, 30, 40, 50) # in percentage


all_BEC_cap, all_BSC_cap = [], []
for cap in CAPACITIES:
	cap = cap/100
	print("capacity:", cap)
	# Find epsilon and p for the given capacity
	epsilon = 1 - cap
	BSC_channel = BSC_with_cap(cap)
	p = BSC_channel["trans"][0][1]
	
	# BEC
	BEC_cap = split_BEC_all(MAX_n, epsilon) # returns the arrays of capacities 
						# for all n up to Max_n

	# BSC
	BSC_cap = []
	for n in range(0, MAX_n+1):
		print("n=", n)
		N = 2**n
		arr_of_cap = np.zeros(N+1) # just to use the indices from 1 to N

		find_capacity_BSC = split_BSC(n, p)
		for i in range(1, N+1):
			arr_of_cap[i] = find_capacity_BSC(i)
		
		BSC_cap.append(arr_of_cap)
	
	
	all_BEC_cap.append(BEC_cap)
	all_BSC_cap.append(BSC_cap)


# We now have a list of lists of np.arrays
# The first dimension is for CAPACITIES
# The second for n
# The third for i




for cap in all_BSC_cap[4]:
	print(cap)












# ## Plot each

# # BEC
# folder_by_capacity = "BEC/by_capacity/"
# folder_by_n = "BEC/by_n/"

# for cap, BEC_cap in zip(CAPACITIES, all_BEC_cap): # for each cap in CAPACITIES
# 	for n, arr_of_cap in enumerate(BEC_cap): # for each n
# 		label = "BEC("+ str(epsilon) +") ; I(W) = " + str(cap/100) + " ; n = " + str(n)
# 		plt.plot(arr_of_cap, "b.", label=label)
# 		plt.legend()
# 		figure_path = folder_by_capacity + "BEC_with_cap_" + str(cap) + "/BEC_" + str(cap) + "_" + str(n)
# 		plt.savefig(figure_path)
# 		figure_path = folder_by_n + "BEC_for_n_" + str(n) + "/BEC_" + str(n) + "_" + str(cap)
# 		plt.savefig(figure_path)
# 		plt.close()


# # BSC
# folder_by_capacity = "BSC/by_capacity/"
# folder_by_n = "BSC/by_n/"

# for cap, BSC_cap in zip(CAPACITIES, all_BSC_cap): # for each cap in CAPACITIES
# 	for n, arr_of_cap in enumerate(BSC_cap): # for each n
# 		label = "BSC("+ str(p) +") ; I(W) = " + str(cap/100) + " ; n = " + str(n)
# 		plt.plot(arr_of_cap, "b.", label=label)
# 		plt.legend()
# 		figure_path = folder_by_capacity + "BSC_with_cap_" + str(cap) + "/BSC_" + str(cap) + "_" + str(n)
# 		plt.savefig(figure_path)
# 		figure_path = folder_by_n + "BSC_for_n_" + str(n) + "/BSC_" + str(n) + "_" + str(cap)
# 		plt.savefig(figure_path)
# 		plt.close()





# ## Plot both together
# folder_by_capacity = "comparison/by_capacity/"
# folder_by_n = "comparison/by_n/"

# for cap, BEC_cap, BSC_cap in zip(CAPACITIES, all_BEC_cap, all_BSC_cap): # for each cap in CAPACITIES
# 	for n, (BEC_arr_of_cap, BSC_arr_of_cap) in enumerate(zip(BEC_cap, BSC_cap)): # for each n
# 		label = "BEC("+ str(epsilon) +") ; I(W) = " + str(cap/100) + " ; n = " + str(n)
# 		plt.plot(BEC_arr_of_cap, "r.", label=label)
# 		label = "BSC("+ str(p) +") ; I(W) = " + str(cap/100) + " ; n = " + str(n)
# 		plt.plot(BSC_arr_of_cap, "b.", label=label)
# 		plt.legend()
# 		figure_path = folder_by_capacity + "comparison_with_cap_" + str(cap) + "/comparison_" + str(cap) + "_" + str(n)
# 		plt.savefig(figure_path)
# 		figure_path = folder_by_n + "comparison_for_n_" + str(n) + "/comparison_" + str(n) + "_" + str(cap)
# 		plt.savefig(figure_path)
# 		plt.close()


# ## Plot their difference
# folder_by_capacity = "difference/by_capacity/"
# folder_by_n = "difference/by_n/"
# all_difference_cap = []
# for cap, BEC_cap, BSC_cap in zip(CAPACITIES, all_BEC_cap, all_BSC_cap): # for each cap in CAPACITIES
# 	difference_cap = []
# 	for n, (BEC_arr_of_cap, BSC_arr_of_cap) in enumerate(zip(BEC_cap, BSC_cap)): # for each n
# 		difference = BEC_arr_of_cap - BSC_arr_of_cap
# 		difference_cap.append(difference)
# 		# plot the positive values in red, negative in blue, and zeros in black
# 		pos_indices, neg_indices, zero_indices = [], [], []
# 		pos_difference, neg_difference, zero_difference = [], [], []
# 		for index, diff in enumerate(difference):
# 			if abs(diff) < .0000000001:
# 				zero_indices.append(index)
# 				zero_difference.append(diff)
# 			elif diff > 0:
# 				pos_indices.append(index)
# 				pos_difference.append(diff)
# 			elif diff < 0:
# 				neg_indices.append(index)
# 				neg_difference.append(diff)

# 		plt.plot(zero_indices, zero_difference, "k.", label="BEC = BSC")
# 		plt.plot(pos_indices, pos_difference, "r.", label="BEC > BSC")
# 		plt.plot(neg_indices, neg_difference, "b.", label="BEC < BSC")

# 		title = "BEC("+ str(epsilon) +") - BSC("+ str(p) +"); I(W) = " + str(cap/100) + " ; n = " + str(n)
# 		plt.title(title)
# 		plt.legend()

# 		figure_path = folder_by_capacity + "difference_with_cap_" + str(cap) + "/difference_" + str(cap) + "_" + str(n)
# 		plt.savefig(figure_path)
# 		figure_path = folder_by_n + "difference_for_n_" + str(n) + "/difference_" + str(n) + "_" + str(cap)
# 		plt.savefig(figure_path)
# 		plt.close()

# 	all_difference_cap.append(difference_cap)



# ## Sort them and write into a file
# # We will have tuples (index, capacity) for each channel, the associated differences
# sorted_all_BEC_cap = []
# sorted_all_BSC_cap = []

# for cap, BEC_cap, BSC_cap in zip(CAPACITIES, all_BEC_cap, all_BSC_cap): # for each cap in CAPACITIES
# 	sorted_BEC_cap, sorted_BSC_cap = [], []
# 	for n, (BEC_arr_of_cap, BSC_arr_of_cap) in enumerate(zip(BEC_cap, BSC_cap)): # for each n
	
# 		arr = [(index, value) for index,value in enumerate(BEC_arr_of_cap)]
# 		arr.sort(key=second, reverse=True)
# 		sorted_BEC_cap.append(arr)
# 		arr = [(index, value) for index,value in enumerate(BSC_arr_of_cap)]
# 		arr.sort(key=second, reverse=True)
# 		sorted_BSC_cap.append(arr)
	
# 	sorted_all_BEC_cap.append(sorted_BEC_cap)
# 	sorted_all_BSC_cap.append(sorted_BSC_cap)

# newline = "\n"
# text = ""
# for n in range(MAX_n+1):
# 	N = 2**n
# 	text += "\t\t\t\t\t\t\t\t n = " + str(n) + " \t\t\t\t\t\t\t\t"
# 	text += newline + newline
# 	text += "I(W)" + "\t"
# 	for cap in CAPACITIES:
# 		text += "\t  " + str(cap) + "\t\t\t"
# 	text += newline
# 	text += "\t"
# 	for cap in CAPACITIES:
# 		text += "     " + "BEC\t" + "BSC\t" + "\t"
# 	text += newline
# 	for i in range(N+1): # do not include the index 0, it has the smallest cap
# 		text += "\t"
# 		for j in range(len(CAPACITIES)):
# 			bec_index, _ = sorted_all_BEC_cap[j][n][i]
# 			bsc_index, _ = sorted_all_BSC_cap[j][n][i]
# 			if bec_index != bsc_index:
# 				text += "  x  "
# 			else:
# 				text += "     "
# 			text += str(bec_index) + "\t\t" + str(bsc_index) + "\t\t"
# 			#text += "\t"
# 		text += newline
# 	text += newline + newline + newline + newline

# print(text)

# file = open("order/order.txt", "w")
# file.write(text)
# file.close()








# BSC = [ 0.00025358771032091276
# , 	 0.026880728341002635
# , 	 0.04320428207700999
# , 	 0.3342994780517927
# , 	 0.0661600475206453
# , 	 0.41542770743350155
# , 	 0.5059577568478162
# , 	 0.8994682775253903
# , 	 0.08825114105506404
# , 	 0.482419736723375
# , 	 0.5839818405280466
# , 	 0.9336317559149389
# , 	 0.6817271581587627
# , 	 0.9617551780211729
# , 	 0.97669203150614
# , 	 0.9997862431760989
# ]

# BEC = [ 1.52587890625e-05
# , 	 0.0077972412109375
# , 	 0.0146636962890625
# , 	 0.2275238037109375
# , 	 0.0366363525390625
# , 	 0.3461761474609375
# , 	 0.4673004150390625
# , 	 0.8998870849609375
# , 	 0.1001129150390625
# , 	 0.5326995849609375
# , 	 0.6538238525390625
# , 	 0.9633636474609375
# , 	 0.7724761962890625
# , 	 0.9853363037109375
# , 	 0.9922027587890625
# , 	 0.9999847412109375
# ]

# comp = [b-a for a,b in zip(BSC, BEC)]


# #plt.plot(comp, "b.", markersize=4, label="BEC - BSC ; I(W) = .5 ; n = 4")
# #plt.legend()
# #plt.savefig("comparaison_2")
# #plt.show()

