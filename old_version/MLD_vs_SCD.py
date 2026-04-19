import decoder
import scd
import encoder
from channels import *
import matplotlib.pyplot as plt

n = 3
W = BSC_X
p = 0.11003
order = [8, 7, 6, 4, 5, 3, 2, 1]
arr_MLD , arr_SCD = [], []
for i in range(len(order)):
    print(i+1)
    indices = order[:i+1]
    A = encoder.indextoindicator(n, indices)
    encode = encoder.coset_encoder(n, A)
    MLD = decoder.MLD_BSC(n, i+1, p, encode)
    SCD = decoder.SCD(W, n, A)
    arr_MLD.append(MLD)
    arr_SCD.append(SCD)
#    break


for MLD, SCD in zip(arr_MLD, arr_SCD):
    print(MLD, SCD)

ind = [i for i in range(1, len(order)+1)]
plt.plot(ind, arr_MLD, "b.", label="MLD")
plt.plot(ind, arr_SCD, "r+", label="SCD")
plt.legend()
plt.show()

# A = np.concatenate((np.zeros(int(N/2)), np.ones(int(N/2))))
# # print(A)
# p = .5
# print(SCD(BSC(p), n, A))
# print(MLD_BSC(n, int(N/2), p, encoder=coset_encoder(n, A)))
