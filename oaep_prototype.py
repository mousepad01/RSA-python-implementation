from MGF1_prototype import mgf1_sha1
from MGF1_prototype import mgf1_sha256

import secrets


def oaep_encode(msg_string, final_len = 512, hash_len = 32):

    # aplicare padding

    '''msg_file = open("oaep_input.txt")

    msg_string = msg_file.readline()

    final_len = 512  # lungimea in biti a stringului final
    hash_len = 32  # lungimea in biti a hash ului dat de sha256'''

    # convertesc mesajul intr un string ce imita reprezentarea binara a string ului

    msg_b_list = bytearray(msg_string, 'ascii')
    msg_b_str = ''.join([format(ch, '08b') for ch in msg_b_list])

    # aplic padding cu un 1 si mai multi de 0

    msg_b_str += '1'

    msg_b_str += '0' * (final_len - len(msg_b_str) - hash_len) * 8

    msg_w0 = int(msg_b_str, 2)

    # generare seed random

    seed = secrets.randbits(hash_len * 8)

    # execut algoritmul

    masked_message = mgf1_sha256(str(seed), final_len - hash_len) ^ msg_w0

    masked_seed = mgf1_sha256(str(masked_message), hash_len) ^ seed

    padded_message = (masked_message << (hash_len * 8)) | masked_seed

    return padded_message


def oaep_decode(padded_message, final_len = 512, hash_len = 32):

    # decodare padding

    masked_message_decoded = padded_message >> (hash_len * 8)
    masked_seed_decoded = padded_message & (2 ** (hash_len * 8) - 1)

    seed_decoded = mgf1_sha256(str(masked_message_decoded), hash_len) ^ masked_seed_decoded

    msg_w0_decoded = mgf1_sha256(str(seed_decoded), final_len - hash_len) ^ masked_message_decoded

    # elimin 0 urile si acel 1, adaugate la finalul mesajului

    while msg_w0_decoded & 1 == 0:
        msg_w0_decoded >>= 1

    msg_w0_decoded >>= 1

    # convertesc mesajul in forma initiala

    msg_b_str_decoded = str(bin(msg_w0_decoded))[2:]
    msg_decoded = ''

    temp_l = len(msg_b_str_decoded)

    while temp_l > 0:

        msg_decoded += chr(int(msg_b_str_decoded[max(temp_l - 8, 0):], 2))

        msg_b_str_decoded = msg_b_str_decoded[:max(temp_l - 8, 0)]
        temp_l -= 8

    msg_decoded = msg_decoded[::-1]

    return msg_decoded















