# get key size from user
#use miller rabin primality test to generate prime number
#make the private key and public key
#encrypt and decrypt the message using the keys
# show the encrypted and decrypted message

import random
import secrets
secret = secrets.SystemRandom()

def square_and_multiply(base, exponent, modulus):
    result = 1
    base = base % modulus
    while exponent > 0:
        if (exponent % 2) == 1:
            result = (result * base) % modulus
        exponent = exponent >> 1
        base = (base * base) % modulus
    return result

def miller_rabin(n, k=20):
    d = n - 1
    r = 0
    while d % 2 == 0:
        d //= 2
        r += 1

    for _ in range(k):
        a = random.randint(2, n - 2)
        x = square_and_multiply(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = square_and_multiply(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


## I now need to generate two primes p and q, and then compute n = p * q. Also need φ(n) = (p-1)(q-1). Also e such that 1 < e < φ(n) and gcd(e, φ(n)) = 1. Finally d such that d ≡ e^(-1) (mod φ(n)).

def prime_generation(key_size):
    total = 0
    while True:
        p = secret.getrandbits(key_size)
        if p % 2 == 0:
            p += 1
        if miller_rabin(p):
            # print(f"Generated prime number p: {p}")
            # print(f"Total attempts to generate prime: {total}")
            return p
        else: 
            total += 1

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def mod_inverse(e, phi):
    original_phi = phi
    x0, x1 = 0, 1
    if phi == 1:
        return 0
    while e > 1:
        q = e // phi
        e, phi = phi, e % phi
        x0, x1 = x1 - q * x0, x0
    if x1 < 0:
        x1 += original_phi
    return x1



def generate_keys(key_size):
    p = prime_generation(key_size)
    q = prime_generation(key_size)
    n = p * q
    phi = (p - 1) * (q - 1)

    e = 65537
    if gcd(e, phi) != 1:
        raise ValueError("e and φ(n) are not coprime.")

    d = mod_inverse(e, phi)

    return (e, d, n)

# print(generate_keys(256))


def message_to_int(message):
    content = int.from_bytes(message.encode('utf-8'), 'big')
    return content

def int_to_message(content):
    message = content.to_bytes((content.bit_length() + 7) // 8, 'big').decode('utf-8')
    return message


def encrypt(message, e, n):
    cyphertext = square_and_multiply(message, e, n)
    return cyphertext

def decrpyt(cypertext, d, n):
    message = square_and_multiply(cypertext, d, n)
    return message



def main():
    e, d, n = generate_keys(256)
    print(f"Public key: (e={e}, n={n})")
    print(f"Private key: (d={d}, n={n})")
    int_message = message_to_int("hello world")
    print(int_message)
    cyphertext = encrypt(int_message, e, n)
    print(f"Encrypted message: {cyphertext}")
    message_int = decrpyt(cyphertext, d, n)
    print(f"Decrypted message: {message_int}")
    message = int_to_message(message_int)
    print(message)

main()