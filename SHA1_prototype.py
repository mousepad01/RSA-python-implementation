def left_rotate(x, k):  # rotatie considerand reprezentarea pe 32 biti
    return ((x << k) & (2 ** x.bit_length() - k)) + (((((2 ** 32 - 1) >> (32 - k)) << (32 - k)) & x) >> (32 - k))


msg_file = open('msg_for_hash.txt')
msg_string = msg_file.readline()

msg = int(msg_string[:len(msg_string)])

msg_b_length = msg.bit_length()

msg = (msg << 1) + 1   # adaug 1 la finalul repr bin a mesajului

# preprocesez mesajul pentru a avea lungimea congruenta cu 0 mod 512

while msg.bit_length() % 512 != 448:
    msg <<= 1

msg <<= 64

msg += msg_b_length

# sparg in bucati de 512 biti si execut algoritmul

h0 = 0x67452301
h1 = 0xEFCDAB89
h2 = 0x98BADCFE
h3 = 0x10325476
h4 = 0xC3D2E1F0

chunk_mask = 2 ** 512 - 1
w_mask = 2 ** 32 - 1

while msg.bit_length() > 0:

    chunk = msg & chunk_mask

    w = []

    i = 0

    while chunk.bit_length() > 0:

        w.append(chunk & w_mask)

        chunk >>= 32

    for i in range(16, 80):
        w.append(left_rotate(w[i - 3] ^ w[i - 8] ^ w[i - 14] ^ w[i - 16], 1))

    a = h0
    b = h1
    c = h2
    d = h3
    e = h4

    f = 0
    k = 0

    for i in range(80):

        if 0 <= i < 20:

            f = (b & c) | ((not b) & c)

            k = 0x5A827999

        elif 20 <= i < 40:

            f = b ^ c ^ d

            k = 0x6ED9EBA1

        elif 40 <= i < 60:

            f = (b & c) | (b & d) | (c & d)

            k = 0x8F1BBCDC

        elif 60 <= i < 80:

            f = b ^ c ^ d

            k = 0xCA62C1D6

        new_val = left_rotate(a, 5) + f + e + k + w[i]
        e = d
        d = c
        c = left_rotate(b, 30)
        b = a
        a = new_val

    h0 += a
    h1 += b
    h2 += c
    h3 += d
    h4 += e

    msg >>= 512

hash_value = (h0 << 128) + (h1 << 96) + (h2 << 64) + (h3 << 32) + h4

print(hex(hash_value))







