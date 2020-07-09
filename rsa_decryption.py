import time
import sys
sys.setrecursionlimit(100000)


def egcd(a, b): # algoritm copiat euclid extins
    x = 0
    y = 1
    u = 1
    v = 0
    while a != 0:
        q = b // a
        r = b % a
        m = x - u * q
        n = y - v * q
        b = a
        a = r
        x = u
        y = v
        u = m
        v = n
    return x


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


# ---------------------------------- main ---------------------------------------

privk = open('private_keys.txt')

auxp = privk.readline()
p = int(auxp[:len(auxp) - 1])

auxq = privk.readline()
q = int(auxq[:len(auxq)])

pubk = open("public_key.txt")

auxn = pubk.readline()
n = int(auxn[:len(auxn) - 1])

auxe = pubk.readline()
e = int(auxe[:len(auxe)])

print('decrypting...')
t = time.time()

d = egcd(e, (p - 1) * (q - 1))

while d < 0:
    d += (p - 1) * (q - 1)

crypted_packages = []

crypted_message = open('cfile.txt')

auxnpackages = crypted_message.readline()
npackages = int(auxnpackages[:len(auxnpackages) - 1])

for i in range(npackages):

    auxpackage = crypted_message.readline()
    crypted_packages.append(int(auxpackage[:len(auxpackage) - 1]))

auxpackage = crypted_message.readline()
crypted_packages.append(int(auxpackage[:len(auxpackage)]))

decrypted_packages = []

for i in range(npackages + 1):
    decrypted_packages.append(str(logpow(d, crypted_packages[i], n) % n))

string_decrypted_message = ''

for i in range(npackages + 1):
    string_decrypted_message = string_decrypted_message + decrypted_packages[i][1:len(decrypted_packages[i]) - 1]

lenght_string_decrypted_message = len(string_decrypted_message)

final_decrypted = ''

for i in range(0, lenght_string_decrypted_message, 3):
    final_decrypted = final_decrypted + chr(int(string_decrypted_message[i:i + 3]))

decryped_message_file = open('dfile.txt', 'w')
decryped_message_file.write(final_decrypted)
print('message decrypted --> found in dfile.txt (', time.time() - t, 'seconds )')
input('done. Press any KEY to continue')
