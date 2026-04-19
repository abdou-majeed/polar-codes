from transitions import *
from utils import *
import decoder
import scd
from math import sqrt
from channels import *




# take U uniform
# find X
# choose Y randomly using chann trans
# decode for u_i
# if error, add to error prob
# compare with Z(WNi)



def montecarlo(channel, n, i):
    W = channel
    N = 2**n
    UtoX = make_UtoX(n)
    

    error = 0
    iter = 100000
    for _ in range(iter):
        U = np.random.randint(0, 2**N)
        X = UtoX(U)
        X_vec = np.array(dectobinary(X, N))
        # if W is BSC
        p = W["trans"][0][1]
        random = np.random.choice((0, 1), N, p=(1-p,p))
        alpha = random.sum()
        Y_vec = xor(X_vec, random)

        U_vec = np.array(dectobinary(U, N))
        U_minus_vec = U_vec[:i-1]
        u_i = U_vec[i-1]

        L = scd.compute_L(W, Y_vec, U_minus_vec)
        if L >=1 :
            pred_u_i = 0
        else:
            pred_u_i = 1
        

        if u_i == 0:
            L = 1/L
        L = sqrt(L)
        error += L
        prob = 0

    return error / iter




# def f(p):
#     return 2 * sqrt(p * (1-p))

# p = .11003
# W = BSC_X
# n = 0
# N = 2**n
# i = 1

# print(montecarlo(W, n, i), f(p))


W = BSC_X
n = 3
N = 2**n
x = np.zeros(N+1)
for i in range(1, N+1):
    x[i] = 1 - montecarlo(W, n, i)


print(x)
import matplotlib.pyplot as plt
plt.plot(x, 'b.')
plt.show()