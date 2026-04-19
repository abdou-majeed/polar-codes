from utils import *
from transitions import *
from channels import *

def WNi(channel, Y_vec, U_minus_vec, U_i):
    W = channel
    N = len(Y_vec)
    n = int(log(N))
    i = len(U_minus_vec) + 1
    UtoY = make_UtoY(n, W)
    Y = binarytodec(Y_vec)


    if n == 0:
        U = binarytodec([U_i])
        return UtoY(U, Y)

    if i == N:
        U_vec = list(U_minus_vec) + [U_i]
        U = binarytodec(U_vec)
        return (1 / 2**(N-1)) * UtoY(U,Y)

    prob = 0
    U1i = list(U_minus_vec) + [U_i]
    for U_plus in range(2**(N-i)):
        U_vec = U1i + dectobinary(U_plus, N-i)
        U = binarytodec(U_vec)
        prob += (1 / 2**(N-1)) * UtoY(U, Y)
    return prob



def brute_L(channel, Y_vec, U_minus_vec):
    W = channel
    N = len(Y_vec)
    n = int(log(N))
    i = len(U_minus_vec) + 1

    a = WNi(W, Y_vec, U_minus_vec, U_i=0)
    b = WNi(W, Y_vec, U_minus_vec, U_i=1)

    if b == 0:
        return 1 # because a > b
    return a / b



def test_WNi():
    W = BSC_X
    p = .1103


    # n = 0

    # Y_vec = np.array([0])
    # U_minus_vec = np.array([])

    # U_i = 0
    # expected = 1-p
    # res = WNi(W, Y_vec, U_minus_vec, U_i)
    # print("Y=" + str(Y_vec) + " U_minus=" + str(U_minus_vec) + " U_i=" + str(U_i) + "\t\t" + \
    #       "Expected: " + str(expected) + " Got: " + str(res))
    # U_i = 1
    # expected = p
    # res = WNi(W, Y_vec, U_minus_vec, U_i)
    # print("Y=" + str(Y_vec) + " U_minus=" + str(U_minus_vec) + " U_i=" + str(U_i) + "\t\t" + \
    #       "Expected: " + str(expected) + " Got: " + str(res))

    # Y_vec = np.array([1])
    # U_minus_vec = np.array([])

    # U_i = 0
    # expected = p
    # res = WNi(W, Y_vec, U_minus_vec, U_i)
    # print("Y=" + str(Y_vec) + " U_minus=" + str(U_minus_vec) + " U_i=" + str(U_i) + "\t\t" + \
    #       "Expected: " + str(expected) + " Got: " + str(res))
    # U_i = 1
    # expected = 1-p
    # res = WNi(W, Y_vec, U_minus_vec, U_i)
    # print("Y=" + str(Y_vec) + " U_minus=" + str(U_minus_vec) + " U_i=" + str(U_i) + "\t\t" + \
    #       "Expected: " + str(expected) + " Got: " + str(res))


    # n = 1

    # Y_vec = np.array([0,1])
    # U_minus_vec = np.array([0])
    # expected = 0.5 * p * (1-p)

    # U_i = 0
    # res = WNi(W, Y_vec, U_minus_vec, U_i)
    # print("Y=" + str(Y_vec) + " U_minus=" + str(U_minus_vec) + " U_i=" + str(U_i) + "\t\t" + \
    #       "Expected: " + str(expected) + " Got: " + str(res))
    # U_i = 1
    # res = WNi(W, Y_vec, U_minus_vec, U_i)
    # print("Y=" + str(Y_vec) + " U_minus=" + str(U_minus_vec) + " U_i=" + str(U_i) + "\t\t" + \
    #       "Expected: " + str(expected) + " Got: " + str(res))

    # Y_vec = np.array([1,1])
    # U_minus_vec = np.array([0])

    # U_i = 0
    # expected = 0.5 * p**2
    # res = WNi(W, Y_vec, U_minus_vec, U_i)
    # print("Y=" + str(Y_vec) + " U_minus=" + str(U_minus_vec) + " U_i=" + str(U_i) + "\t\t" + \
    #       "Expected: " + str(expected) + " Got: " + str(res))
    # U_i = 1
    # expected = 0.5 * (1-p)**2
    # res = WNi(W, Y_vec, U_minus_vec, U_i)
    # print("Y=" + str(Y_vec) + " U_minus=" + str(U_minus_vec) + " U_i=" + str(U_i) + "\t\t" + \
    #       "Expected: " + str(expected) + " Got: " + str(res))

    # n = 1

    # Y_vec = np.array([0,0])
    # U_minus_vec = np.array([])

    # U_i = 0
    # expected = 0.5 * (p**2 + (1-p)**2)
    # res = WNi(W, Y_vec, U_minus_vec, U_i)
    # print("Y=" + str(Y_vec) + " U_minus=" + str(U_minus_vec) + " U_i=" + str(U_i) + "\t\t" + \
    #       "Expected: " + str(expected) + " Got: " + str(res))
    # U_i = 1
    # expected = p * (1-p)
    # res = WNi(W, Y_vec, U_minus_vec, U_i)
    # print("Y=" + str(Y_vec) + " U_minus=" + str(U_minus_vec) + " U_i=" + str(U_i) + "\t\t" + \
    #       "Expected: " + str(expected) + " Got: " + str(res))

    # Y_vec = np.array([0,1])
    # U_minus_vec = np.array([])

    # U_i = 0
    # expected = p * (1-p)
    # res = WNi(W, Y_vec, U_minus_vec, U_i)
    # print("Y=" + str(Y_vec) + " U_minus=" + str(U_minus_vec) + " U_i=" + str(U_i) + "\t\t" + \
    #       "Expected: " + str(expected) + " Got: " + str(res))
    # U_i = 1
    # expected = 0.5 * (p**2 + (1-p)**2)
    # res = WNi(W, Y_vec, U_minus_vec, U_i)
    # print("Y=" + str(Y_vec) + " U_minus=" + str(U_minus_vec) + " U_i=" + str(U_i) + "\t\t" + \
    #       "Expected: " + str(expected) + " Got: " + str(res))


    # Y_vec = np.array([0,1])
    # U_minus_vec = np.array([1])

    # U_i = 0
    # expected = 0.5 * p**2
    # res = WNi(W, Y_vec, U_minus_vec, U_i)
    # print("Y=" + str(Y_vec) + " U_minus=" + str(U_minus_vec) + " U_i=" + str(U_i) + "\t\t" + \
    #       "Expected: " + str(expected) + " Got: " + str(res))
    # U_i = 1
    # expected = 0.5 * (1-p)**2
    # res = WNi(W, Y_vec, U_minus_vec, U_i)
    # print("Y=" + str(Y_vec) + " U_minus=" + str(U_minus_vec) + " U_i=" + str(U_i) + "\t\t" + \
    #       "Expected: " + str(expected) + " Got: " + str(res))


def test_brute_L():
    W = BSC_X
    p = .1103
    n = 0

#     Y_vec = np.array([0])
#     U_minus_vec = np.array([])

#     expected = (1-p) / p
#     res = brute_L(W, Y_vec, U_minus_vec)
#     print("Y=" + str(Y_vec) + " U_minus=" + str(U_minus_vec) + "\t\t" + \
#           "Expected: " + str(expected) + " Got: " + str(res))

#     Y_vec = np.array([1])
#     U_minus_vec = np.array([])

#     expected = p / (1-p)
#     res = brute_L(W, Y_vec, U_minus_vec)
#     print("Y=" + str(Y_vec) + " U_minus=" + str(U_minus_vec) + "\t\t" + \
#           "Expected: " + str(expected) + " Got: " + str(res))


    Y_vec = np.array([0,0])
    U_minus_vec = np.array([0])
    res = brute_L(W, Y_vec, U_minus_vec)
    print("Y=" + str(Y_vec) + " U_minus=" + str(U_minus_vec) + "\t\t" + \
        #   "Expected: " + str(expected) +
          " Got: " + str(res))
    U_minus_vec = np.array([1])
    res = brute_L(W, Y_vec, U_minus_vec)
    print("Y=" + str(Y_vec) + " U_minus=" + str(U_minus_vec) + "\t\t" + \
        #   "Expected: " + str(expected) +
          " Got: " + str(res))

    Y_vec = np.array([0,1])
    U_minus_vec = np.array([0])
    res = brute_L(W, Y_vec, U_minus_vec)
    print("Y=" + str(Y_vec) + " U_minus=" + str(U_minus_vec) + "\t\t" + \
        #   "Expected: " + str(expected) +
          " Got: " + str(res))
    U_minus_vec = np.array([1])
    res = brute_L(W, Y_vec, U_minus_vec)
    print("Y=" + str(Y_vec) + " U_minus=" + str(U_minus_vec) + "\t\t" + \
        #   "Expected: " + str(expected) +
          " Got: " + str(res))

    Y_vec = np.array([1,0])
    U_minus_vec = np.array([0])
    res = brute_L(W, Y_vec, U_minus_vec)
    print("Y=" + str(Y_vec) + " U_minus=" + str(U_minus_vec) + "\t\t" + \
        #   "Expected: " + str(expected) +
          " Got: " + str(res))
    U_minus_vec = np.array([1])
    res = brute_L(W, Y_vec, U_minus_vec)
    print("Y=" + str(Y_vec) + " U_minus=" + str(U_minus_vec) + "\t\t" + \
        #   "Expected: " + str(expected) +
          " Got: " + str(res))

    Y_vec = np.array([1,1])
    U_minus_vec = np.array([0])
    res = brute_L(W, Y_vec, U_minus_vec)
    print("Y=" + str(Y_vec) + " U_minus=" + str(U_minus_vec) + "\t\t" + \
        #   "Expected: " + str(expected) +
          " Got: " + str(res))
    U_minus_vec = np.array([1])
    res = brute_L(W, Y_vec, U_minus_vec)
    print("Y=" + str(Y_vec) + " U_minus=" + str(U_minus_vec) + "\t\t" + \
        #   "Expected: " + str(expected) +
          " Got: " + str(res))



# test_WNi()

test_brute_L()