import random
import time


def get_omega(p, n):
    """
    Given a field of size p, this method returns an nth root of unity.
    """
    x = random.randint(0, p-1)
    y = pow(x, (p-1)//n, p)
    if y == 1:
        return get_omega(p, n)
    assert pow(y, n, p) == 1
    return y


def fft(n, A, omega, p):
    """
    Given coefficients A of polynomial this method does FFT and returns
    the evaluation of the polynomial at [omega^0, omega^(n-1)]

    If the polynomial is a0*x^0 + a1*x^1 + ... + an*x^n then the coefficients
    list is of the form [a0, a1, ... , an].
    """
    # Check if n is a power of 2.
    x = len(A)
    assert n == len(A)
    assert not (n & (n-1))
    assert not (x & (x-1))

    if n == 1:
        return A
    # print(n)
    B = A[0::2]
    C = A[1::2]
    B_bar = fft(n//2, B, pow(omega, 2, p), p)
    C_bar = fft(n//2, C, pow(omega, 2, p), p)
    A_bar = [0]*(n)
    for j in range(n):
        k = (j % (n//2))
        A_bar[j] = (B_bar[k] + ((pow(omega, j, p))*C_bar[k]) % p) % p
    return A_bar


def generate_polynomial(n):
    """
    Returns a list of coefficients denoting a polynomial.
    If the polynomial is a0*x^0 + a1*x^1 + ... + an*x^n then the output list
    is of the form [a0, a1, ... , an].

    """
    return [random.randint(0, i) for i in range(random.randint(1, n))]


def test_correctness(coefficients, omega, fft_result, p):
    """
    This method verifies the output generated by FFT by evaluating
    the polynomial at the coefficients.

    In order to save time, it verifies only 100 points from the FFT output
    after evaluating them at the coefficients.
    """
    assert len(coefficients) == len(fft_result)
    n = len(fft_result)

    # Test on 100 random points
    points = [random.randint(0, n) for i in range(100)]
    c = 0
    for i in points:
        y = 0
        for k in range(n):
            if coefficients[k] != 0:
                y = (y + (coefficients[k] * pow(omega, i*k, p)) % p) % p
                # print("####", y, coefficients[k], pow(omega, i*k, p), k, p)
        # print(y, fft_result[i], i)
        c += 1
        print(c, "points verfied")
        assert y == fft_result[i]

# This `r` is the order of BLS12-381, also the base field of 
# the JubJub curve. `n` is a large power of 2 that divides `(r-1)` 
r = 0x73eda753299d7d483339d80809a1d80553bda402fffe5bfeffffffff00000001
n = pow(2, 17)

coefficients = generate_polynomial(1000)
padded_coefficients = coefficients + ([0] * (n-len(coefficients)))
# print(len(padded_coefficients), n)
# print(padded_coefficients)

s = time.time()
omega = get_omega(r, n)
e = time.time()
print("OMEGA", omega, "TIME:", e - s)

s = time.time()
output = fft(n, padded_coefficients, omega, r)
e = time.time()
print("FFT completed", "TIME:", e - s)
test_correctness(padded_coefficients, omega, output, r)
