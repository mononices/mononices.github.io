---
title: Anti-Fermat
layout: post
---

[zer0pts 2022]

*I invented Anti-Fermat Key Generation for RSA cipher since I'm scared of the Fermat's Factorization Method.*

[Download challenge](https://github.com/kanin9/ctf/files/8313836/challenge.zip)

Description gives us a hint, pointing to Fermat's Factorization method, but the solution boils down to solving quadratic equation.

From the start we are greeted with this chunk of code and output in hex format

```python
from Crypto.Util.number import isPrime, getStrongPrime
from gmpy import next_prime
from secret import flag

# Anti-Fermat Key Generation
p = getStrongPrime(1024)
q = next_prime(p ^ ((1<<1024)-1))
n = p * q
e = 65537

# Encryption
m = int.from_bytes(flag, 'big')
assert m < n
c = pow(m, e, n)

print('n = {}'.format(hex(n)))  # 0x1ffc7dc6b9667b0dcd00d6ae92...
print('c = {}'.format(hex(c)))  # 0x60160bfed79384048d0d46b807...
```

Note that `q` is the next prime after the number created by flipping all bits of `p`, so we can rewrite `q` as follows:

**q = (2^1024 - 1) - p + error** 
 
With this information we can factorize N by incrementing over the error value, and then solving quadratic equation for one of the factors 

**p((2^1024 - 1) - p + error) = N**

**-p^2 + p(error + 2^1024 - 1) - N = 0**


```python
from Crypto.Util.number import long_to_bytes
from gmpy2 import next_prime
from values import n, c, modinv
from math import isqrt


P = 0
e = 65537

for error in range(0, 1 << 13):
    xor = (1 << 1024) - 1
    b = xor + error
    D = b * b - 4 * n
    sqr = isqrt(D)
    if sqr * sqr == D:
        x1 = (-b + sqr) // -2
        x2 = (-b - sqr) // -2
        if x1 * (n // x1) == n:
            print("Value found ", x1)
            P = x1
        if x2 * (n // x2) == n:
            print("Value found ", x2)
            P = x2

Q = n // P
phi = (P - 1) * (Q - 1)
d = modinv(e, phi)
print(long_to_bytes(pow(c, d, n)))
```

And that's about it:

![image](https://user-images.githubusercontent.com/101967194/159232684-9a1bfb65-7283-4843-8f83-7c130c586c15.PNG)

---

**zer0pts{F3rm4t,y0ur_m3th0d_n0_l0ng3r_w0rks.y0u_4r3_f1r3d}**
