# utils.py

# TODO
# inttolabel, labeltoint,
# entropy given distr, cond entr


import numpy as np
from math import log2


def log(p):
    """Takes a real "p" >= 0 and returns "0" if p = 0, and log2(p) otherwise"""
    assert p >= 0
    if p == 0:
        return 0
    return log2(p)


def plogp(p):
    """Takes a real "p" >= 0 and returns "0" if p = 0, and plog2(p) otherwise"""
    assert p >= 0
    if p == 0:
        return 0
    return p * log2(p)


def xor(A, B):
    return (A+B) % 2
# xor = np.logical_xor


def matmul(*args):
    """Performs the matrix multiplication in F2. Takes the same inputs as np.matmul"""
    return np.matmul(*args) % 2


def matpower(*args):
    """Performs the matrix power in F2. Takes the same inputs as np.linalg.matrix_power"""
    return np.linalg.matrix_power(*args) % 2


def dectobase(dec, base, size):
    """Converts from base 10 to base 'base'.
	Takes a decimal representation "dec" of a nonnegative integer, converts it into base "base", and returns a list of length "size" containing the digits in base "base".
	Inputs
	- dec:  int >= 0
	- base: int >= 2
	- size: int, ignored if too small to represent the number in base "base"
	Returns
	- digits: list (of integers), each entry is 0 <= entry < base
	"""

    assert type(dec) == int and dec >= 0
    assert type(base) == int and base >= 2
    assert type(size) == int

    digits = []
    while dec != 0:
        digits.append(dec % base)
        dec = dec // base
    digits = digits[::-1]

    nb_of_leading_zeros = max(0, (size - len(digits)))
    digits = [0] * nb_of_leading_zeros + digits
    return digits


def dectobinary(dec, size):
    """Converts from base 10 to base 2.
	Takes a decimal representation "dec" of a nonnegative integer and returns its binary representation as a list of length "size" containing the binary digits.
	Inputs
	- dec:  int >= 0
	- size: int, ignored if too small to represent the number in base 2
	Returns
	- bits: list (of integers: 0 or 1)
	"""

    assert type(dec) == int and dec >= 0
    assert type(size) == int

    binary_str = bin(dec)[2:]  # bin(x) comes with leading 0x
    bits = [int(char) for char in binary_str]

    nb_of_leading_zeros = max(0, (size - len(bits)))
    bits = [0] * nb_of_leading_zeros + bits
    return bits


def basetodec(digits, base):
    """Returns a decimal representention of a nonnegative number in base 'base'.
	'digits' is an iterable. It is the representation of the nonnegative integer in base 'base'.
	Inputs
	- digits: list (of integers), each entry is 0 <= entry < base
	- base:	int >= 2
	Returns
	- dec: int >= 0
	"""

    # accept any iterable for digits ?
    # assert isinstance(digits, iterable)
    # check range of each entry?
    assert type(base) == int and base >= 2

    # print("digits", digits)

    dec = 0
    base_powered = 1  # b**0
    for digit in digits[::-1]:  # starts from least significant bit
        dec += digit * base_powered
        base_powered *= base
    
    # print("dec", dec)
    return int(dec)


def binarytodec(bits):
    """Returns the decimal representation of a nonnegative binary number.
	'bits' is an iterable. It is the binary representation of a nonnegative integer.
	Input
	- bits: list (of integers: 0 or 1)
	Returns
	- dec: int >= 0
	"""

    # accept any iterable for bits ?
    return basetodec(bits, 2)


def bissection_search(interval, function, goal, epsilon=10 ** (-12)):
    """Performs the bissection search.
	Inputs
	- interval: tuple (a, b)
	- function: an increasing function defined on [a, b]. For a decreasing function on [a, b], pass (b, a) as interval.
	- goal	  : the value of f(x) we wish to approximate
	- epsilon : desired accuracy of approximation
	Returns:
	- x : such that |function(x) - goal| < epsilon (by default: epsilon = 1 / 10**12) 
"""

    # assertions ?
    # stop if not converging? not improving?
    (low, high) = interval
    f = function

    x = (low + high) / 2
    #	print("low", low, "high", high, "x", x)
    while abs(f(x) - goal) >= epsilon:
        #		print("f(x) =", f(x))
        if goal < f(x):
            high = x
        else:
            low = x
        x = (low + high) / 2
    #		print("low", low, "high", high, "x", x)
    # print("f(x) =", f(x))
    return x
