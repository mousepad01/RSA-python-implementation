maxdim = 2 ** 32
mask32 = maxdim - 1


def left_rotate(x, ct):  # rotatie pe 32 biti
    return ((x << ct) & mask32) | (x >> 32 - ct)


msg_file = open('msg_for_hash.txt')
msg_string = msg_file.readline()

msg_b_list = bytearray(msg_string, 'ascii')
msg = ''.join([format(x, '08b') for x in msg_b_list])

msg_b_length = len(msg)

msg += '1'  # adaug 1 la finalul repr bin a mesajului

# preprocesez mesajul pentru a avea lungimea congruenta cu 0 mod 512

while len(msg) % 512 != 448:
    msg += '0'

msg += str(format(msg_b_length, '064b'))

# sparg in bucati de 512 biti si execut algoritmul

h = [0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476, 0xC3D2E1F0]

while len(msg) > 0:

    chunk = msg[:512]

    w = []

    while len(chunk) > 0:

        w.append(int(chunk[:32], 2))

        chunk = chunk[32:]

    for i in range(16, 80):
        w.append(left_rotate(w[i - 3] ^ w[i - 8] ^ w[i - 14] ^ w[i - 16], 1) & mask32)

    a = h[0]
    b = h[1]
    c = h[2]
    d = h[3]
    e = h[4]

    f = 0
    k = 0

    for i in range(80):

        if 0 <= i < 20:

            f = (b & c) ^ (~b & d)

            k = 0x5A827999

        elif 20 <= i < 40:

            f = b ^ c ^ d

            k = 0x6ED9EBA1

        elif 40 <= i < 60:

            f = (b & c) ^ (b & d) ^ (c & d)

            k = 0x8F1BBCDC

        elif 60 <= i < 80:

            f = b ^ c ^ d

            k = 0xCA62C1D6

        temp1 = (left_rotate(a, 5) + f + e + k + w[i]) & mask32
        e = d
        d = c
        c = left_rotate(b, 30)
        b = a
        a = temp1

    h[0] += a
    h[1] += b
    h[2] += c
    h[3] += d
    h[4] += e

    h[0] &= mask32
    h[1] &= mask32
    h[2] &= mask32
    h[3] &= mask32
    h[4] &= mask32

    msg = msg[512:]

hash_value = (h[0] << 128) | (h[1] << 96) | (h[2] << 64) | (h[3] << 32) | h[4]

print(hex(hash_value))






