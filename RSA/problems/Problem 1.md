
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

