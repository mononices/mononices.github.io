---
  title: Frozen Cake Writeup [CakeCTF 2022]
  layout: post
  tags: crypto warmup cakectf
---

*Oh your cake is frozen. please warm it up and get the first cake.*

```python
from Crypto.Util.number import getPrime
import os

flag = os.getenv("FLAG", "FakeCTF{warmup_a_frozen_cake}")
m = int(flag.encode().hex(), 16)

p = getPrime(512)
q = getPrime(512)

n = p*q

print("n =", n)
print("a =", pow(m, p, n))
print("b =", pow(m, q, n))
print("c =", pow(m, n, n))
```

This task was built around general intuition of how RSA works, especially the decryption part.

To solve this challenge you need to learn about generalised form of Fermat's Little Theorem, here it is:

**a^(ф(n)) = 1 mod n** *(n here is not necessarily prime)* 

And as we remember totient function for n is just **(p-1)(q-1)**

We can factor totient as **n - p - q - 1**

To substract exponents we should divide one ciphertext by another, but how can we do it in a modulo scenario?
For this purposes exist modular inverses. Dividing `c` value by `a` and `b`, or more specifically multiplying `c` by modular inverses of `a` and `b`, we get almost here, now we need to somehow calculate m. Let's take a side look on what we already figured out.

**d = m^(n - p - q)**

**dm = 1 (mod n)**

Last equation seems familiar ain't so?
Yes, m is just modular inverse for our value d modulo n

So far, so good, we get a solution.

```python
n = 101205131618457490641888226172378900782027938652382007193297646066245321085334424928920128567827889452079884571045344711457176257019858157287424646000972526730522884040459357134430948940886663606586037466289300864147185085616790054121654786459639161527509024925015109654917697542322418538800304501255357308131
a = 38686943509950033726712042913718602015746270494794620817845630744834821038141855935687477445507431250618882887343417719366326751444481151632966047740583539454488232216388308299503129892656814962238386222995387787074530151173515835774172341113153924268653274210010830431617266231895651198976989796620254642528
b = 83977895709438322981595417453453058400465353471362634652936475655371158094363869813512319678334779139681172477729044378942906546785697439730712057649619691929500952253818768414839548038664187232924265128952392200845425064991075296143440829148415481807496095010301335416711112897000382336725454278461965303477
c = 21459707600930866066419234194792759634183685313775248277484460333960658047171300820279668556014320938220170794027117386852057041210320434076253459389230704653466300429747719579911728990434338588576613885658479123772761552010662234507298817973164062457755456249314287213795660922615911433075228241429771610549

d = (c * pow(a, -1, n) * pow(b, -1, n)) % n
m = pow(d, -1, n)
print(bytes.fromhex(hex(m)[2:]))
```
If you read my explanation all the way through, try solution for yourself. Don't be a coward. 🤠




