from utils import *
from channels import *


def select_odd(vec):
    new = []
    for i in range(0, len(vec), 2):
        new.append(vec[i])
    return np.array(new)

def select_even(vec):
    new = []
    for i in range(1, len(vec), 2):
        new.append(vec[i])
    return np.array(new)


def compute_L(channel, Y_vec, U_minus_vec):
    W = channel
    N = len(Y_vec)
    i = len(U_minus_vec) + 1

    if N == 1:
        y = Y_vec[0]
        a = W["trans"][0][y]
        b = W["trans"][1][y]
        # print("Y_vec", Y_vec, "U_minus", U_minus_vec)
        # print(b, type(b))
        if b == 0:
            return 1
#        res = a / b
#       if (abs(res - 1) < 0.0001):
#        	if np.random.rand() > .5:
#        		return 1
#        	else:
#        		return 
        return a / b

    if i % 2 == 0:
        # then i = 2j
        Y_slice1 = Y_vec[:int(N/2)]
        Y_slice2 = Y_vec[int(N/2):]
        U_slice = U_minus_vec[:-1]
        # assert len(U_slice) == i-2
        U_odd = select_odd(U_slice)
        U_even = select_even(U_slice)
        a = compute_L(W, Y_slice1, xor(U_odd, U_even))
        b = compute_L(W, Y_slice2, U_even)
        exp = 1 - (2 * U_minus_vec[-1])
        return (a**exp) * b

    else:
        # then i = 2j - 1
        j = int((i+1)/2)
        Y_slice1 = Y_vec[:int(N/2)]
        Y_slice2 = Y_vec[int(N/2):]
        U_slice = U_minus_vec
        # assert len(U_slice) == i-1
        U_odd = select_odd(U_slice)
        U_even = select_even(U_slice)
        a = compute_L(W, Y_slice1, xor(U_odd, U_even))
        b = compute_L(W, Y_slice2, U_even)
        return (a*b + 1) / (a + b)


def insert(x, dic, keys):
	if len(keys) == 1:
		dic[keys[0]] = x
	elif keys[0] in dic.keys():
		dic[keys[0]] = insert(x, dic[keys[0]], keys[1:])
	else:
		dic[keys[0]] = insert(x, {}, keys[1:])

	return dic


def new_dynamic_L():
    L_dict = {}
    def dynamic_L(channel, Y_vec, U_minus_vec):
        nonlocal L_dict
        W = channel
        N = len(Y_vec)
        i = len(U_minus_vec) + 1

        if N == 1:
            y = Y_vec[0]
            a = W["trans"][0][y]
            b = W["trans"][1][y]
            if b == 0:
                return 1
            return a / b
        
        if i % 2 == 0:
            # then i = 2j
            j =  int(i/2)
            a = L_dict.get(int(N/2), {}).get(j, {}).get(0)
            b = L_dict.get(int(N/2), {}).get(j, {}).get(1)

            Y_slice1 = Y_vec[:int(N/2)]
            Y_slice2 = Y_vec[int(N/2):]
            U_slice = U_minus_vec[:-1]
            U_odd = select_odd(U_slice)
            U_even = select_even(U_slice)

            if a == None:
                a = dynamic_L(W, Y_slice1, xor(U_odd, U_even))
                L_dict = insert(a, L_dict, (int(N/2), j, 0))
            if b == None:
                b = dynamic_L(W, Y_slice2, U_even)
                L_dict = insert(b, L_dict, (int(N/2), j, 1))
            exp = 1 - (2 * U_minus_vec[-1])
            return (a**exp) * b

        else:
            # then i = 2j - 1
            j = int((i+1)/2)
            a = L_dict.get(int(N/2), {}).get(j, {}).get(0)
            b = L_dict.get(int(N/2), {}).get(j, {}).get(1)

            Y_slice1 = Y_vec[:int(N/2)]
            Y_slice2 = Y_vec[int(N/2):]
            U_slice = U_minus_vec
            U_odd = select_odd(U_slice)
            U_even = select_even(U_slice)

            if a == None:
                a = dynamic_L(W, Y_slice1, xor(U_odd, U_even))
                L_dict = insert(a, L_dict, (int(N/2), j, 0))
            if b == None:
                b = dynamic_L(W, Y_slice2, U_even)
                L_dict = insert(b, L_dict, (int(N/2), j, 1))
            return (a*b + 1) / (a + b)

    return dynamic_L





def test_dynamic_L():
    W = BSC_X
    p = .1103
    n = 0
    dynamic_L = new_dynamic_L()

    Y_vec = np.array([0])
    U_minus_vec = np.array([])

    expected = (1-p) / p
    res = dynamic_L(W, Y_vec, U_minus_vec)
    print("Y=" + str(Y_vec) + " U_minus=" + str(U_minus_vec) + "\t\t" + \
          "Expected: " + str(expected) + " Got: " + str(res))

    dynamic_L = new_dynamic_L()
    Y_vec = np.array([1])
    U_minus_vec = np.array([])

    expected = p / (1-p)
    res = dynamic_L(W, Y_vec, U_minus_vec)
    print("Y=" + str(Y_vec) + " U_minus=" + str(U_minus_vec) + "\t\t" + \
          "Expected: " + str(expected) + " Got: " + str(res))



    dynamic_L = new_dynamic_L()
    Y_vec = np.array([0,0])
    U_minus_vec = np.array([0])
    res = dynamic_L(W, Y_vec, U_minus_vec)
    print("Y=" + str(Y_vec) + " U_minus=" + str(U_minus_vec) + "\t\t" + \
        #   "Expected: " + str(expected) +
          " Got: " + str(res))
    dynamic_L = new_dynamic_L()
    U_minus_vec = np.array([1])
    res = dynamic_L(W, Y_vec, U_minus_vec)
    print("Y=" + str(Y_vec) + " U_minus=" + str(U_minus_vec) + "\t\t" + \
        #   "Expected: " + str(expected) +
          " Got: " + str(res))

    dynamic_L = new_dynamic_L()
    Y_vec = np.array([0,1])
    U_minus_vec = np.array([0])
    res = dynamic_L(W, Y_vec, U_minus_vec)
    print("Y=" + str(Y_vec) + " U_minus=" + str(U_minus_vec) + "\t\t" + \
        #   "Expected: " + str(expected) +
          " Got: " + str(res))
    dynamic_L = new_dynamic_L()
    U_minus_vec = np.array([1])
    res = dynamic_L(W, Y_vec, U_minus_vec)
    print("Y=" + str(Y_vec) + " U_minus=" + str(U_minus_vec) + "\t\t" + \
        #   "Expected: " + str(expected) +
          " Got: " + str(res))

    dynamic_L = new_dynamic_L()
    Y_vec = np.array([1,0])
    U_minus_vec = np.array([0])
    res = dynamic_L(W, Y_vec, U_minus_vec)
    print("Y=" + str(Y_vec) + " U_minus=" + str(U_minus_vec) + "\t\t" + \
        #   "Expected: " + str(expected) +
          " Got: " + str(res))
    dynamic_L = new_dynamic_L()
    U_minus_vec = np.array([1])
    res = dynamic_L(W, Y_vec, U_minus_vec)
    print("Y=" + str(Y_vec) + " U_minus=" + str(U_minus_vec) + "\t\t" + \
        #   "Expected: " + str(expected) +
          " Got: " + str(res))

    dynamic_L = new_dynamic_L()
    Y_vec = np.array([1,1])
    U_minus_vec = np.array([0])
    res = dynamic_L(W, Y_vec, U_minus_vec)
    print("Y=" + str(Y_vec) + " U_minus=" + str(U_minus_vec) + "\t\t" + \
        #   "Expected: " + str(expected) +
          " Got: " + str(res))
    dynamic_L = new_dynamic_L()
    U_minus_vec = np.array([1])
    res = dynamic_L(W, Y_vec, U_minus_vec)
    print("Y=" + str(Y_vec) + " U_minus=" + str(U_minus_vec) + "\t\t" + \
        #   "Expected: " + str(expected) +
          " Got: " + str(res))







def test_compute_L():
    W = BSC_X
    p = .1103
    n = 0

    # Y_vec = np.array([0])
    # U_minus_vec = np.array([])

    # expected = (1-p) / p
    # res = compute_L(W, Y_vec, U_minus_vec)
    # print("Y=" + str(Y_vec) + " U_minus=" + str(U_minus_vec) + "\t\t" + \
    #       "Expected: " + str(expected) + " Got: " + str(res))

    # Y_vec = np.array([1])
    # U_minus_vec = np.array([])

    # expected = p / (1-p)
    # res = compute_L(W, Y_vec, U_minus_vec)
    # print("Y=" + str(Y_vec) + " U_minus=" + str(U_minus_vec) + "\t\t" + \
    #       "Expected: " + str(expected) + " Got: " + str(res))



    Y_vec = np.array([0,0])
    U_minus_vec = np.array([0])
    res = compute_L(W, Y_vec, U_minus_vec)
    print("Y=" + str(Y_vec) + " U_minus=" + str(U_minus_vec) + "\t\t" + \
        #   "Expected: " + str(expected) +
          " Got: " + str(res))
    U_minus_vec = np.array([1])
    res = compute_L(W, Y_vec, U_minus_vec)
    print("Y=" + str(Y_vec) + " U_minus=" + str(U_minus_vec) + "\t\t" + \
        #   "Expected: " + str(expected) +
          " Got: " + str(res))

    Y_vec = np.array([0,1])
    U_minus_vec = np.array([0])
    res = compute_L(W, Y_vec, U_minus_vec)
    print("Y=" + str(Y_vec) + " U_minus=" + str(U_minus_vec) + "\t\t" + \
        #   "Expected: " + str(expected) +
          " Got: " + str(res))
    U_minus_vec = np.array([1])
    res = compute_L(W, Y_vec, U_minus_vec)
    print("Y=" + str(Y_vec) + " U_minus=" + str(U_minus_vec) + "\t\t" + \
        #   "Expected: " + str(expected) +
          " Got: " + str(res))

    Y_vec = np.array([1,0])
    U_minus_vec = np.array([0])
    res = compute_L(W, Y_vec, U_minus_vec)
    print("Y=" + str(Y_vec) + " U_minus=" + str(U_minus_vec) + "\t\t" + \
        #   "Expected: " + str(expected) +
          " Got: " + str(res))
    U_minus_vec = np.array([1])
    res = compute_L(W, Y_vec, U_minus_vec)
    print("Y=" + str(Y_vec) + " U_minus=" + str(U_minus_vec) + "\t\t" + \
        #   "Expected: " + str(expected) +
          " Got: " + str(res))

    Y_vec = np.array([1,1])
    U_minus_vec = np.array([0])
    res = compute_L(W, Y_vec, U_minus_vec)
    print("Y=" + str(Y_vec) + " U_minus=" + str(U_minus_vec) + "\t\t" + \
        #   "Expected: " + str(expected) +
          " Got: " + str(res))
    U_minus_vec = np.array([1])
    res = compute_L(W, Y_vec, U_minus_vec)
    print("Y=" + str(Y_vec) + " U_minus=" + str(U_minus_vec) + "\t\t" + \
        #   "Expected: " + str(expected) +
          " Got: " + str(res))




# test_compute_L()
# print("")
# test_dynamic_L()
