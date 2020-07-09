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


def ciur():
    global erath
    global primes

    erath[0] = 1
    erath[1] = 1

    i = 2
    while i <= 500:
        if erath[i] == 0:

            j = i * i
            while j <= 250000:

                erath[j] = 1
                j += i

        i += 1

    for i in range(2, 250000):
        if erath[i] == 0:
            primes.append(i)


def bignumgen():
    global testlen
    global end_forbidden_lenght
    global start_forbidden_lenght

    import secrets

    sg = secrets.SystemRandom()

    ncif = sg.randint(600,650)

    if testlen == True and start_forbidden_lenght <= ncif <= end_forbidden_lenght: # pentru a nu avea 2 nr prime cu nr asemanator de cifre

        st_add = end_forbidden_lenght - ncif + 1

        ncif += sg.randint(st_add, st_add + 4)

    bignumber = sg.randint(1, 9) # prima cifra a numarului

    while ncif != 0:

        cif = sg.randint(0, 9)
        while ncif == 1 and cif & 1 == 0:
            cif = sg.randint(0, 9)

        bignumber *= 10
        bignumber += cif

        ncif -= 1

    return bignumber


def checkdiv(x):
    global primes

    for i in range(20000):
        if x % primes[i] == 0:
            return 0

    return 1


def primegen():
    global primelist

    candidate = bignumgen()

    while checkdiv(candidate) == 0:
        candidate = bignumgen()
    #candidate = int(input())
    #print(checkdiv(candidate))

    mod = candidate
    t = time.time()
    #print('candidate lenght: ',lenght(candidate),end = ' ')

    n_minus_1 = candidate - 1

    exp = 0

    while n_minus_1 & 1 == 0:
        n_minus_1 //= 2
        exp += 1

    dp = n_minus_1

    import random

    alist = primes[:15] + [primes[random.randint(15, 22000)] for i in range(35)]
    #print(alist)
    #print(candidate,'\n', exp, d)
    lalist = len(alist)

    for i in range(lalist):
        a = alist[i]
        #print('a =',a,end = ' ')

        ad = logpow(dp, a, mod)

        if ad != 1 and ad != candidate - 1:

            #print(' a la d nu este nici 1 nici -1 ')

            r_found = False

            for r in range(1, exp):

                ad *= ad
                ad %= candidate

                if ad == candidate - 1:
                    r_found = True

            if not r_found:
                #print(' a la d*2^r nu este -1 pt oricare r')
                #print(time.time() - t)
                return -1

        #print('a nu este martor , se trece la urmatorul')
    return candidate


# ----------------------------------- main ------------------------------------


print('initialization...')

t = time.time()

erath = [0 for i in range(250001)]
primes = []
ciur()
print('prime set initialized (', time.time() - t, ' seconds )')
print('\n')

testlen = False
end_forbidden_lenght = -1
start_forbidden_lenght = -1

t = time.time()

print('generating first prime...')
p = primegen()
while p == -1:
    p = primegen()

privk = open("private_keys.txt", 'w')
privk.write(str(p))
privk.write('\n')
print('first prime generated --> line 1 in private_keys.txt (', time.time() - t, ' seconds )')
print('\n')

testlen = True
start_forbidden_lenght = lenght(p) - 3
end_forbidden_lenght = lenght(p) + 3

t = time.time()

print('generating second prime...')
q = primegen()
while q == -1:
    q = primegen()

privk.write(str(q))
print('second prime generated --> line 2 in private_keys.txt (', time.time() - t, ' seconds )')
print('\n')

n = p * q
e = 65537
# e = int(input())

pubk = open("public_key.txt", 'w')
pubk.write(str(n))
pubk.write('\n')
pubk.write(str(e))
print('public key n generated --> line 1 in public_key.txt')
print('public key e uploaded: e =', e)

input('done. Press any KEY to continue')

