"""Utility functions for polar code construction and analysis over GF(2).

This module provides the foundational primitives used throughout the polar
codes project, an implementation of Erdal Arikan's channel polarization
framework ("Channel polarization: A method for constructing capacity-achieving
codes for symmetric binary-input discrete memoryless channels," 2009).

Polar codes operate in the binary field GF(2) = {0, 1}, where addition is
XOR and multiplication is AND. The encoding operation x = u * G_N is a
matrix-vector product over GF(2), where G_N = B_N * F^(⊗n) is
Arikan's generator matrix of size N = 2^n.

This module provides:

    - **Information-theoretic functions**: ``safe_log2`` and ``p_log2_p``
      implement the standard convention 0 * log(0) = 0 for computing
      Shannon entropy and channel capacity.

    - **GF(2) linear algebra**: ``f2_add``, ``f2_matmul``, and
      ``f2_matrix_power`` perform addition and matrix multiplication
      modulo 2, as required by the Arikan construction.

    - **Binary representation**: ``int_to_bits``, ``bits_to_int``,
      ``int_to_digits``, and ``digits_to_int`` convert between
      non-negative integers and their digit-vector representations.
      These are needed because the polar code framework constantly maps
      between message vectors u in {0,1}^N (stored as bit arrays) and
      their integer indices in 0..2^N - 1.

    - **Array partitioning**: ``partition_by_indicator``,
      ``partition_odd_even``, and ``indices_to_indicator`` split arrays
      according to indicator vectors. ``partition_by_indicator`` is how
      the rows of G_N get separated into the information set A and the
      frozen set A^c -- the fundamental step of polar code construction.

    - **Numerical search**: ``bisection_search`` is a general-purpose
      bisection method for finding the input to a monotonic function
      that produces a desired output value. In this project it is used
      to find channel parameters (e.g., BSC crossover probability)
      matching a target capacity or Bhattacharyya parameter, but it
      works for any monotonic function.

    - **Deep equality**: ``deep_equal`` checks whether two objects are
      structurally identical, element by element, even when one is a
      Python list and the other is a NumPy array. It exists because
      comparing a list to a NumPy array with ``==`` does not return a
      single True/False -- it returns an array. This function walks
      through both structures recursively and returns a single bool.

References:
    Arikan, E. (2009). Channel polarization: A method for constructing
    capacity-achieving codes for symmetric binary-input discrete
    memoryless channels. IEEE Transactions on Information Theory, 55(7),
    3051-3073. arXiv:0807.3917.

Example usage::

    from utils import int_to_bits, bits_to_int, f2_matmul

    # Convert message index to bit vector
    u_vec = int_to_bits(5, width=4)   # [0, 1, 0, 1]

    # Encode: x = u * G_N over GF(2)
    x_vec = f2_matmul(u_vec, G_N)

    # Convert codeword back to index
    x_index = bits_to_int(x_vec)      # integer
"""
from collections.abc import Callable, Iterable
from math import log2

import numpy as np


# ---------------------------------------------------------------------------
#  Deep equality
# ---------------------------------------------------------------------------

def deep_equal(a: object, b: object) -> bool:
    """Recursively compare two structures for element-wise equality.

    Supports nested combinations of lists, tuples, NumPy arrays, and
    numeric scalars. Two structures are equal if they have the same
    shape and all corresponding leaf elements satisfy ``==``.

    This function exists to bridge Python lists and NumPy arrays, which
    behave differently under ``==`` (NumPy returns element-wise arrays,
    not a single bool). It is used in test assertions and in encoder
    precondition checks.

    Warning:
        Do not pass strings. Strings are iterable and will be compared
        character-by-character against the other argument, which is
        almost never the intended behavior.

    Args:
        a: A scalar, list, tuple, or NumPy array.
        b: A scalar, list, tuple, or NumPy array.

    Returns:
        True if ``a`` and ``b`` are structurally identical, False
        otherwise.

    Examples:
        >>> deep_equal([1, 2, 3], np.array([1, 2, 3]))
        True
        >>> deep_equal([[1, 0], [0, 1]], np.eye(2, dtype=int))
        True
        >>> deep_equal([1, 2], [1, 2, 3])
        False
    """
    if isinstance(a, Iterable) and isinstance(b, Iterable):
        return len(a) == len(b) and all(
            deep_equal(ai, bi) for ai, bi in zip(a, b)
        )
    return a == b


# ---------------------------------------------------------------------------
#  Information-theoretic functions
# ---------------------------------------------------------------------------

def safe_log2(p: float) -> float:
    """Compute log base 2, returning 0.0 when p is zero.

    Implements the information-theoretic convention that log(0) = 0,
    consistent with the limit p * log(p) -> 0 as p -> 0+. Used in
    channel capacity and entropy computations.

    Args:
        p: A non-negative real number (typically a probability).

    Returns:
        log2(p) if p > 0, or 0.0 if p == 0.

    Raises:
        AssertionError: If p < 0.
    """
    assert p >= 0
    if p == 0:
        return 0.0
    return log2(p)


def p_log2_p(p: float) -> float:
    """Compute p * log2(p), returning 0.0 when p is zero.

    Used to compute Shannon entropy: H(p) = -p_log2_p(p) - p_log2_p(1-p).

    Args:
        p: A non-negative real number (typically a probability).

    Returns:
        p * log2(p) if p > 0, or 0.0 if p == 0.

    Raises:
        AssertionError: If p < 0.
    """
    assert p >= 0
    if p == 0:
        return 0.0
    return p * log2(p)


# ---------------------------------------------------------------------------
#  GF(2) linear algebra
# ---------------------------------------------------------------------------

def f2_add(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Compute element-wise addition over GF(2) (i.e., XOR).

    In the binary field GF(2) = {0, 1}, addition is defined as
    exclusive-or: 0+0=0, 0+1=1, 1+0=1, 1+1=0.

    Args:
        a: A NumPy array of 0s and 1s.
        b: A NumPy array of 0s and 1s, same shape as ``a``.

    Returns:
        Element-wise (a + b) mod 2.
    """
    return (a + b) % 2


def f2_matmul(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Compute matrix multiplication over GF(2).

    Performs standard matrix multiplication followed by reduction
    modulo 2. Used for encoding (x = u * G_N) and for verifying
    generator matrix properties (G * G_inv == I over GF(2)).

    Args:
        a: A 1-D or 2-D NumPy array of 0s and 1s.
        b: A 1-D or 2-D NumPy array of 0s and 1s, with compatible
            shape for matrix multiplication.

    Returns:
        The matrix product (a @ b) mod 2.
    """
    return np.matmul(a, b) % 2


def f2_matrix_power(matrix: np.ndarray, exponent: int) -> np.ndarray:
    """Compute a matrix raised to an integer power over GF(2).

    Kept for completeness alongside ``f2_add`` and ``f2_matmul``.

    Args:
        matrix: A square 2-D NumPy array of 0s and 1s.
        exponent: A non-negative integer.

    Returns:
        matrix^exponent mod 2.
    """
    return np.linalg.matrix_power(matrix, exponent) % 2


# ---------------------------------------------------------------------------
#  Base conversions
# ---------------------------------------------------------------------------

def int_to_base(value: int, base: int, width: int) -> list[int]:
    """Convert a non-negative integer to a list of digits in a given base.

    The result is zero-padded on the left to have at least ``width``
    elements. If the number requires more than ``width`` digits, all
    digits are returned and a ``ValueError`` is raised.

    Args:
        value: A non-negative integer to convert.
        base: The target base (>= 2).
        width: The minimum length of the returned digit list (>= 1).

    Returns:
        A list of integers, each in the range [0, base), representing
        ``value`` in the given base, most-significant digit first.

    Raises:
        AssertionError: If value < 0, base < 2, or width < 1.
        ValueError: If ``value`` requires more than ``width`` digits
            in the given base. This means the caller provided an
            insufficient width for the value being converted.

    Examples:
        >>> int_to_base(13, 2, 8)
        [0, 0, 0, 0, 1, 1, 0, 1]
        >>> int_to_base(0, 10, 3)
        [0, 0, 0]
    """
    assert value >= 0 and base >= 2 and width >= 1

    digits = []
    remaining = value
    while remaining != 0:
        digits.append(remaining % base)
        remaining = remaining // base
    digits = digits[::-1]

    if len(digits) > width:
        raise ValueError(
            f"Value {value} requires {len(digits)} digits in base {base}, "
            f"but width={width} was requested"
        )

    padding = max(0, width - len(digits))
    digits = [0] * padding + digits

    return digits


def int_to_bits(value: int, width: int) -> list[int]:
    """Convert a non-negative integer to a binary digit list.

    Equivalent to ``int_to_base(value, 2, width)`` but uses Python's
    built-in format string for efficiency, since this is the most
    frequently called function in the project.

    Args:
        value: A non-negative integer to convert.
        width: The minimum length of the returned bit list.

    Returns:
        A list of 0s and 1s, most-significant bit first, zero-padded
        on the left to at least ``width`` elements.

    Raises:
        AssertionError: If value < 0.
        ValueError: If ``value`` requires more than ``width`` bits.

    Examples:
        >>> int_to_bits(5, 4)
        [0, 1, 0, 1]
        >>> int_to_bits(0, 8)
        [0, 0, 0, 0, 0, 0, 0, 0]
    """
    assert value >= 0

    binary_str = f"{value:0{width}b}"

    if len(binary_str) > width:
        raise ValueError(
            f"Value {value} requires {len(binary_str)} bits, "
            f"but width={width} was requested"
        )

    return [int(c) for c in binary_str]


def base_to_int(digits: list[int], base: int) -> int:
    """Convert a digit list in a given base to a non-negative integer.

    Inverse of ``int_to_base``. Iterates from the least-significant
    digit (last element) to the most-significant (first element).

    Args:
        digits: An iterable of integers, each in [0, base), most-
            significant digit first.
        base: The base of the digit representation (>= 2).

    Returns:
        The non-negative integer represented by ``digits`` in the
        given base.

    Raises:
        AssertionError: If base < 2 or any digit is out of range.

    Examples:
        >>> base_to_int([1, 1, 0, 1], 2)
        13
        >>> base_to_int([0, 0, 0], 10)
        0
    """
    assert base >= 2

    dec = 0
    base_powered = 1  # base**0
    for digit in digits[::-1]:
        assert 0 <= digit < base
        dec += digit * base_powered
        base_powered *= base

    return int(dec)  # avoid numpy integer types


def bits_to_int(bits: list[int]) -> int:
    """Convert a binary digit list to a non-negative integer.

    Equivalent to ``base_to_int(bits, 2)``. Uses Python's built-in
    ``int(..., 2)`` for efficiency, since this is a frequently called
    function in the project.

    Args:
        bits: An iterable of 0s and 1s, most-significant bit first.

    Returns:
        The non-negative integer represented by the bit string.

    Examples:
        >>> bits_to_int([1, 0, 1])
        5
        >>> bits_to_int([0, 0, 0, 0])
        0
    """
    return int("".join(str(b) for b in bits), 2) if bits else 0


# ---------------------------------------------------------------------------
#  Numerical search
# ---------------------------------------------------------------------------

def bisection_search(
    bounds: tuple[float, float],
    func: Callable[[float], float],
    target: float,
    tolerance: float = 1e-12,
    max_iter: int = 1000,
) -> float:
    """Find x such that func(x) is approximately equal to target.

    Uses the bisection method on a monotonic function. The search
    halves the interval at each step until |func(x) - target| is
    within the specified tolerance, or ``max_iter`` iterations are
    reached.

    For a non-decreasing function, pass ``bounds=(low, high)``. For a
    non-increasing function, pass ``bounds=(high, low)`` -- the
    algorithm only checks whether ``target < func(x)`` to decide which
    half to keep, so swapping the endpoints reverses the direction.

    Args:
        bounds: A tuple (a, b) defining the search interval. The
            function must be monotonic between a and b, and ``target``
            must lie within [func(a), func(b)] (or [func(b), func(a)]
            if swapped).
        func: A monotonic function of one float argument.
        target: The desired function value to approximate.
        tolerance: The search stops when |func(x) - target| < tolerance.
            Defaults to 1e-12.
        max_iter: Maximum number of bisection iterations. Defaults to
            1000. Prevents non-termination when ``target`` is outside
            the range of ``func`` on the interval.

    Returns:
        A float x in [min(a, b), max(a, b)] such that
        |func(x) - target| < tolerance.

    Raises:
        ValueError: If the search does not converge within ``max_iter``
            iterations.
    """
    low, high = bounds

    for _ in range(max_iter):
        x = (low + high) / 2
        if abs(func(x) - target) < tolerance:
            return x
        if target < func(x):
            high = x
        else:
            low = x

    raise ValueError(
        f"bisection_search did not converge after {max_iter} iterations"
    )


# ---------------------------------------------------------------------------
#  Array partitioning
# ---------------------------------------------------------------------------

def partition_by_indicator(
    array: np.ndarray,
    indicator: list[int],
) -> tuple[np.ndarray, np.ndarray]:
    """Split an array into two sub-arrays based on a 0/1 indicator.

    Elements at positions where ``indicator`` is 1 go into the first
    output array; elements where it is 0 go into the second. This is
    the mechanism for separating the rows of the generator matrix G_N
    into the information set A and the frozen set A^c.

    When ``array`` is 2-D (e.g., G_N), the split is performed along
    the first axis (rows).

    Args:
        array: A NumPy array of length N.
        indicator: A list of 0s and 1s of length N.

    Returns:
        A tuple (selected, remaining) where ``selected`` contains the
        elements at positions marked 1, and ``remaining`` contains
        the elements at positions marked 0.

    Raises:
        AssertionError: If ``array`` and ``indicator`` differ in length,
            or if any entry of ``indicator`` is not 0 or 1.

    Examples:
        >>> partition_by_indicator(np.array([10, 20, 30, 40]), [1, 0, 1, 0])
        (array([10, 30]), array([20, 40]))
    """
    assert len(array) == len(indicator)

    selected, remaining = [], []
    for i, flag in enumerate(indicator):
        assert flag in (0, 1)
        if flag == 1:
            selected.append(array[i])
        else:
            remaining.append(array[i])

    return np.array(selected), np.array(remaining)


def partition_odd_even(array: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Split an array into odd-indexed and even-indexed entries.

    Uses 1-based indexing to match Arikan's paper conventions: the
    first entry (Python index 0) is considered "odd" (position 1),
    the second entry (Python index 1) is "even" (position 2), etc.

    This means:
        - odd  = array[0], array[2], array[4], ...  (positions 1, 3, 5, ...)
        - even = array[1], array[3], array[5], ...  (positions 2, 4, 6, ...)

    Args:
        array: A NumPy array.

    Returns:
        A tuple (odd, even) of NumPy arrays.

    Examples:
        >>> partition_odd_even(np.array([10, 20, 30, 40]))
        (array([10, 30]), array([20, 40]))
    """
    return array[::2], array[1::2]


def indices_to_indicator(length: int, indices: list[int]) -> list[int]:
    """Convert a list of 1-based indices to a 0/1 indicator vector.

    Returns a list of length ``length`` where position i-1 is 1 if i
    appears in ``indices``, and 0 otherwise. Uses 1-based indexing to
    match Arikan's paper conventions.

    Args:
        length: The length of the output indicator vector (>= 0).
        indices: A list of integers, each satisfying 1 <= index <= length.

    Returns:
        A list of 0s and 1s of the given length.

    Raises:
        AssertionError: If length < 0 or any index is out of range.

    Examples:
        >>> indices_to_indicator(5, [1, 3, 5])
        [1, 0, 1, 0, 1]
        >>> indices_to_indicator(4, [2])
        [0, 1, 0, 0]
    """
    assert length >= 0
    if length == 0:
        return []

    indicator = [0] * length
    for index in indices:
        assert 1 <= index <= length
        indicator[index - 1] = 1

    return indicator
# Content: Structure it by uses. Group them
    # - General
