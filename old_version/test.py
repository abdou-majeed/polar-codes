from utils import dectobinary
import numpy as np

def make_func(n, fourier_spec):
    def f(x):
        # compute parities
        # dot product with fourier spect
        parities = np.zeros(2**n)
        for i in range(2**n):
            binary = dectobinary(i, n)[::-1]
            # print("binary", binary)
            prod = 1
            for j,bit in enumerate(binary):
                if bit == 1:
                    # print("x[j]", x[j])
                    prod *= x[j]
            parities[i] = prod
            # print(parities)
        # print(parities)
        
        return np.dot(fourier_spec, parities)
    return f


def compare(n, f, g):
    epsilon = 10**(-10)
    for i in range(2**n):
        x = np.array(dectobinary(i, n))
        x = -2*x + 1
        if abs(f(x) - g(x)) > epsilon:
            return False
    return True

# f = make_func(2, np.array([1,1,1,1]))
# print(f(np.array([-1,1])))

# g = make_func(2, np.array([1,1,1,1]))
# print(compare(2, f, g))

def max2(x):
    return x.max()

def min2(x):
    return x.min()

min3, max3 = min2, max2

def sel3(x):
    if x[0] == -1:
        return x[1]
    return x[2]

def sorted4(x):
    def asc(a):
        first = True
        for i in a:
            if not first and last > i:
                return False
            first = False
            last = i
        return True
    
    if asc(x) or asc(np.flip(x)):
        return -1
    return 1

def maj5(x):
    if x.sum() > 0:
        return 1
    return -1

# max2
# f = make_func(2, np.array([1/2, 1/2, 1/2, -1/2]))
# print(compare(2, f, max2))

# min2
# f = make_func(2, np.array([-1/2, 1/2, 1/2, 1/2]))
# print(compare(2, f, min2))

# min3
# f =make_func(3, np.array([-3/4]+[1/4]*7))
# print(compare(3, f, min3))

# max3
# f =make_func(3, np.array([3/4, 1/4, 1/4, -1/4, 1/4, -1/4, -1/4, 1/4]))
# print(compare(3, f, max3))

# sel3
# f = make_func(3, np.array([0, 0, 1/2, -1/2, 1/2, 1/2, 0, 0]))
# print(compare(3, f, sel3))

# sorted4
# f = make_func(4, np.array([0, 0, 0, -1/2, 0, 0, -1/2, 0, 0, 1/2, 0, 0, -1/2, 0, 0, 0]))
# print(compare(4, f, sorted4))

# for i in range(2**4):
#     a = np.array(dectobinary(i, 4))
#     a = -2 * a + 1
#     print(a, sorted4(a))


def spectrum_from_degree(n, weights_per_deg):
    spectrum = np.zeros(2**n)
    for i in range(2**n):
        binary = dectobinary(i, n)
        deg = np.array(binary).sum()
        spectrum[i] = weights_per_deg[deg]
    return spectrum

# print(spectrum_from_degree(3, [1/2, 1/4, -1/2, 0]))


# Maj5
spectrum = spectrum_from_degree(5, [0, 3/8, 0, -1/8, 0, 3/8])
f = make_func(5, spectrum)
print(compare(5, f, maj5))

# Maj7
