
# RSA Challenge — “Intercepted Message”

Alex, a junior developer, built a “secure messaging system” using RSA but didn’t follow best practices.
You managed to intercept a message sent between two users.

After analyzing the traffic, you obtained the following values:

```text
n = 2773
e = 17
C = 855
```

Alex claims the system is “unbreakable.”

Recover the original message `M`.
# Notes

* The system uses standard RSA (no padding)
* Message is a small integer
* No tricks beyond weak implementation

---

# What You Should Think

```text
Is n secure enough?
Can I factor it?
What happens after I get p and q?
```

# Goal

```text
Find M
```

```
alhamrizvi@alhams-fedora:~$ python3
Python 3.14.3 (main, Mar 26 2026, 00:00:00) [GCC 15.2.1 20260123 (Red Hat 15.2.1-7)] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from sympy import mod_inverse, factorint
>>> n = 2773
... e = 17
... C = 855
... 
>>> fac = factorint(n)
>>> p, q = list(fac.keys())
>>> phi = (p - 1) * (q - 1)
>>> d = mod_inverse(e, phi)
>>> M = mod_inverse(C, d, n)
Traceback (most recent call last):
  File "<python-input-6>", line 1, in <module>
    M = mod_inverse(C, d, n)
TypeError: mod_inverse() takes 2 positional arguments but 3 were given
>>> M = pow(C, d, n)
>>> print(M)
1029
>>> fac = factorint(2773)
>>> print(fac)
{47: 1, 59: 1}
>>> M = pow(C, d, n)
>>> print(M)
1029

```



<img width="1412" height="619" alt="image" src="https://github.com/user-attachments/assets/fca2be59-50e3-4491-bb6c-284f12228bad" />

