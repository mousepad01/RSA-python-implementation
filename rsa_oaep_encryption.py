import time
import sys
import random

from oaep_prototype import oaep_encode
from MGF1_prototype import sha256

sys.setrecursionlimit(100000)


def lenght(x):

    count = 0

    if x == 0:
        return 1

    while x:
        count += 1
        x //= 10

    return count


def logpow(exp, base, mod):

    base %= mod

    if exp == 0:
        return 1

    if exp == 1:
        return base % mod

    if exp & 1 == 0:
        return logpow(exp // 2, base ** 2, mod) % mod

    if exp & 1 == 1:
        return (base * logpow(exp // 2, base ** 2, mod) % mod) % mod


print('reading message...')
msgfile = open('mfile.txt')
message = msgfile.read()
lm = len(message)

pubk = open("public_key.txt")
privk = open("private_keys.txt")

auxp = privk.readline()
auxq = privk.readline()

auxd = privk.readline()
d = int(auxd[:len(auxd)])

t = time.time()

auxn = pubk.readline()
n = int(auxn[:len(auxn) - 1])

auxe = pubk.readline()
e = int(auxe[:len(auxe)])

# digital signature generator

message_hash = sha256(message)

signature = logpow(d, message_hash, n)

# ---------------------------------

converted_message = ''

for i in range(lm):

    if 0 <= ord(message[i]) <= 9:
        converted_message = converted_message + '00'

    if 10 <= ord(message[i]) <= 99:
        converted_message = converted_message + '0'

    converted_message = converted_message + str(ord(message[i]))

message_packages = []

lmessage = len(converted_message)

nlenght = lenght(n)

lenpackage = random.randint(20, 30)

if lenpackage >= lmessage:

    message_packages.append(converted_message)
else:
    for i in range(0, lmessage, lenpackage):

        message_packages.append(converted_message[i:min(lmessage, i + lenpackage)])

npackages = len(message_packages) - 1

# pentru padding

for i in range(len(message_packages)):
    message_packages[i] = oaep_encode(message_packages[i], 110)

# ----------------------------------------

crypted_packages = []

for i in range(npackages + 1):
    crypted_packages.append(logpow(e, message_packages[i], n) % n)

crypted_file = open("cfile.txt", 'w')

crypted_file.write(str(npackages))
crypted_file.write('\n')

for i in range(npackages + 1):
    crypted_file.write(str(crypted_packages[i]))
    crypted_file.write('\n')

print('message encrypted ---> found in cfile.txt starting with line 1 (', time.time() - t, ' seconds )')

crypted_file.write(str(signature))

print('message signed ---> signature found in last line of cfile.txt')

input('done. Press any KEY to continue')

