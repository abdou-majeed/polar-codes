# channels.py


# TODO:
#	Class Channel
#	Random Symmetric Channel
# Symbol codes for random channels

import numpy as np
from math import sqrt
from utils import log, bissection_search


def BEC(p):
  return {
    "input" : ["0", "1"],
    # "output": ["0", "1", "?"],
    # "trans" : np.array([ [1-p, 0, p], [0, 1-p, p] ])
    "output": ["0", "?", "1"],
    "trans" : np.array([ [1-p, p, 0], [0, p, 1-p] ])
    }

def BSC(p):
  return {
    "input" : ["0", "1"],
    "output": ["0", "1"],
    "trans" : np.array([ [1-p, p], [p, 1-p] ])
  }

BEC_30 	= BEC(.3)
BEC_50 	= BEC(.5)
BEC_70 	= BEC(.7)
BEC_100 = BEC(1)

BSC_30 	= BSC(.3)
BSC_50  = BSC(.5)
BSC_70  = BSC(.7)
BSC_100 = BSC(1)
BSC_X 	= BSC(.11003) # capacity(BSC_X) = capacity(BEC_50) = .5
# (redefined below as BSC_with_cap(0.5))


def raw_capacity(transition):
	"""transition is the transition matrix of a binary channel. Returns the symmetric capacity of the channel.
	- transition: numpy.array with shape (2, cardY)
	Returns
    - cap: float
    """
	# assertions?

	M = transition
	cardX, cardY = 2, M.shape[1]
	
	cap = 0
	for x in range(cardX):
		for y in range(cardY):
			cap += 0.5 * M[x][y] * ( log(M[x][y]) - log(0.5 * M[0][y] + 0.5 * M[1][y]))
	return cap
	
def capacity(channel):
	"""Returns the symmetric capacity of the given binary channel"""
	return raw_capacity(channel["trans"])

def raw_bhatta(transition):
	"""transition is the transition matrix of a binary channel. Returns the bhattacharyya parameter of the channel.
	- transition: numpy.array with shape (2, cardY)
	Returns
    - bhattacharyya: float
    """

	M = transition
	cardY = M.shape[1]
	
	bhattacharyya = 0
	for y in range(cardY):
		bhattacharyya += sqrt(M[0][y] * M[1][y])
	return bhattacharyya

def bhatta(channel):
	"""Returns the bhattacharyya parameter of the given binary channel"""
	return raw_bhatta(channel["trans"])


def BSC_with_cap(cap):
	"""Returns a BSC channel with capacity 'cap' """
	assert 0 <= cap and cap <= 1
	
	# search for p in [0, .5]
	def f(p):
		return capacity(BSC(p))

	# Recall that the capacity decreases with p.
	return BSC( bissection_search( (0.5,0), f, cap) )

BSC_X = BSC_with_cap(.5) # capacity(BSC_X) = capacity(BEC_50) = .5

def BSC_with_bhatta(bhattacharyya):
	"""Returns a BSC channel with the given bhattacharyya parameter"""
	assert bhattacharyya >= 0 and bhattacharyya <= 1
	
	# search for p in [0, .5]
	def f(p):
		return bhatta(BSC(p))

	# bhattacharyya increases with p
	return BSC( bissection_search( (0,0.5), f, bhattacharyya) )


def random_channel(cardY):
  # make cardY uniquely decodable characters
  # compress, symbol code
  # write decoder: inttolabel?
  # generate random transition probabilities

  output = []
  l = (cardY-1) // 10 + 1  # nb of symbols per character
  for i in range(cardY):
    y = "0" * (l - len(str(i))) + str(i) # add leading zeros
    output.append(y)
  
  trans = np.random.sample((2,cardY))
  trans[0] = trans[0] / trans[0].sum()
  trans[1] = trans[1] / trans[1].sum()
  
  return {
    "input" : ["0", "1"],
    "output": output,
    "trans" : trans
  }

RC4 = random_channel(4)
RC7 = random_channel(7)