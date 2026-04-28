# polar-codes (refactoring in progress: it will take a while!)

An implementation of Arıkan's polar codes from first principles.

I wrote this simulation about three years ago when doing research on polar codes.
I am progressively refactoring the code to make it more readable and accessible to general readers.
I will upload the new version progressively.

Polar codes are the first family of error-correcting codes with an explicit construction
that provably achieves the symmetric capacity of any binary-input discrete memoryless channel.
They were introduced by Erdal Arıkan in 2009 and are now part of the 5G NR standard.

This project implements the core building blocks described in
[Arıkan's original paper](https://arxiv.org/abs/0807.3917):
channel models, the generator matrix via multilinear monomials over GF(2),
coset encoding, successive cancellation decoding, maximum-likelihood decoding,
and the channel splitting analysis that demonstrates the polarization phenomenon.


## What this implements

| Component | Description |
|---|---|
| **Channel models** | Binary Symmetric Channel (BSC) and Binary Erasure Channel (BEC), with capacity, Bhattacharyya parameter, and stochastic simulation (`send`). |
| **Generator matrix** | Construction of the polar code generator via multilinear monomials over GF(2). Includes Arıkan's bit-reversal ordering and the inverse generator. |
| **Encoding** | Coset encoder using Arıkan's generator matrix. Supports arbitrary information sets and frozen bit patterns. |
| **Successive cancellation decoding** | Recursive likelihood-ratio computation (the L-values from Arıkan section VII), with both a direct recursive version and a dynamic-programming version that caches intermediate values. |
| **Maximum-likelihood decoding** | BFS-based ML decoder for the BSC that enumerates Hamming balls around received words. |
| **Channel splitting** | BEC splitting via the closed-form recursion. BSC splitting via brute-force computation using the inverse generator. |
| **Transition probabilities** | U to X (encoding), X to Y (channel), and U to Y (composed) mappings for analysis and decoding. |
| **GF(2) arithmetic** | XOR, matrix multiplication, matrix power, base conversion utilities, all over the binary field. |


## Architecture

```
polar-codes/
|-- channels.py              # BSC and BEC channel classes
|-- channel_combination.py   # Generator matrix construction
|-- channel_splitting.py     # Polarization analysis (BEC closed-form, BSC brute-force)
|-- encoder.py               # Coset encoder
|-- decoder.py               # Maximum-likelihood decoder
|-- scd.py                   # Successive cancellation decoder
|-- transitions.py           # U->X, X->Y, U->Y probability mappings
|-- utils.py                 # GF(2) arithmetic and base conversions
|-- experiments/
|   |-- bsc_vs_bec.py        # Compare polarization across channel types and capacities
|   +-- main.py              # Quick demonstration of channel splitting
+-- tests/
    |-- channel_combination_test.py
    |-- encoder_test.py
    +-- utils_test.py
```

The files are best read in this order:

1. `utils.py` — base conversions and GF(2) operations used everywhere
2. `channels.py` — BSC and BEC channel definitions
3. `channel_combination.py` — generator matrix construction
4. `encoder.py` — coset encoding
5. `scd.py` — successive cancellation decoding
6. `decoder.py` — maximum-likelihood decoding
7. `channel_splitting.py` — polarization analysis
8. `transitions.py` — probability mappings


## How it works

Arikan's construction starts from N = 2^n independent copies of a binary channel W
and synthesizes N new channels {W_N^(i)} through a recursive combining and splitting
operation. As N grows, the synthetic channels polarize: a fraction I(W) of them
have capacity approaching 1, and the rest have capacity approaching 0. Encoding sends
data through the near-perfect channels and fixes the others to known (frozen) values.
Decoding proceeds sequentially, estimating each bit using likelihood ratios computed
from the channel outputs and all previously decoded bits.

The generator matrix G_N = B_N F^{⊗n} is built from the kernel F = [[1,0],[1,1]]
via Kronecker powers and bit-reversal permutation. This project constructs G_N
equivalently through multilinear monomials over GF(2), which makes the connection
to Reed-Muller codes explicit: row i of the generator corresponds to the monomial
whose variables are determined by the binary expansion of i.

The successive cancellation decoder computes the likelihood ratio

    L_N^(i)(y, u^{i-1}) = W_N^(i)(y, u^{i-1} | 0) / W_N^(i)(y, u^{i-1} | 1)

recursively, using the relations:

- Odd index:  L = (L_a * L_b + 1) / (L_a + L_b)
- Even index: L = L_a^{1 - 2*u_{i-1}} * L_b

where L_a and L_b come from the two half-size subproblems. The dynamic-programming
version caches these intermediate values to avoid redundant computation.


## Quick start

```bash
git clone https://github.com/abdou-majeed/polar-codes.git
cd polar-codes
pip install numpy matplotlib
```

Run the channel splitting demonstration:

```bash
python experiments/main.py
```

Run the BEC vs BSC polarization comparison:

```bash
python experiments/bsc_vs_bec.py
```

Run the tests:

```bash
python tests/utils_test.py
python tests/channel_combination_test.py
python tests/encoder_test.py
```


## Example: BEC polarization

For a BEC with erasure probability ε = 0.5 (capacity = 0.5), the channel splitting
recursion produces 2^n synthetic channels whose capacities cluster near 0 and 1:

| n | Block length | Channels with capacity > 0.99 | Channels with capacity < 0.01 |
|---|---|---|---|
| 0 | 1 | 0 | 0 |
| 4 | 16 | 5 | 5 |
| 10 | 1024 | ~488 | ~488 |
| 20 | 1048576 | ~524200 | ~524200 |

This is the polarization phenomenon: roughly half the channels become near-perfect
and half become near-useless, matching the channel capacity of 0.5.


## Requirements

- Python 3.8+
- NumPy
- Matplotlib (for experiment plots)


## References

1. E. Arikan, “Channel polarization: A method for constructing capacity-achieving codes
   for symmetric binary-input discrete memoryless channels,” *IEEE Transactions on
   Information Theory*, vol. 55, no. 7, pp. 3051–3073, July 2009.
   [arXiv:0807.3917](https://arxiv.org/abs/0807.3917)

2. I. Tal and A. Vardy, “How to construct polar codes,” *IEEE Transactions on
   Information Theory*, vol. 59, no. 10, pp. 6562–6582, October 2013.
