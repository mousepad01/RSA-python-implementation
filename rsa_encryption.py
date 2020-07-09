import time
import sys
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

t = time.time()

auxn = pubk.readline()
n = int(auxn[:len(auxn) - 1])

auxe = pubk.readline()
e = int(auxe[:len(auxe)])

converted_message = ''

for i in range(lm):

    if 0 <= ord(message[i]) <= 9:
        converted_message = converted_message + '00'

    if 10 <= ord(message[i]) <= 99:
        converted_message = converted_message + '0'

    converted_message = converted_message + str(ord(message[i]))

message_packages = []

lmessage = len(converted_message)

import random

nlenght = lenght(n)

lenpackage = random.randint(20, 30)

if lenpackage >= lmessage:

    aux = str(random.randint(1, 9))
    aux2 = str(random.randint(1, 9))

    message_packages.append(int(aux + converted_message + aux2)) # adaugare cifra nenula la inceputul si sfarsitul blocului
else:
    for i in range(0, lmessage, lenpackage):

        aux = str(random.randint(1, 9))
        aux2 = str(random.randint(1, 9))

        message_packages.append(int(aux + converted_message[i:min(lmessage, i + lenpackage)] + aux2)) # adaugare cifra nenula la inceputul si sfarsitul blocul

npackages = len(message_packages) - 1

crypted_packages = []

for i in range(npackages + 1):
    crypted_packages.append(logpow(e, message_packages[i], n) % n)

crypted_file = open("cfile.txt", 'w')

crypted_file.write(str(npackages))
crypted_file.write('\n')

for i in range(npackages + 1):
    crypted_file.write(str(crypted_packages[i]))
    crypted_file.write('\n')

print('message encrypted ---> found in cfile.txt starting with line 2 (', time.time() - t, ' seconds )')
input('done. Press any KEY to continue')

