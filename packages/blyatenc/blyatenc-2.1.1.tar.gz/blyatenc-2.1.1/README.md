# Blyat encryption/decryption algorithm

from blyatalgorithm import blyatenc

bc = blyatenc.blyatenc()
print(bc.encrypt("Hello world!"))
print(bc.decrypt(":5n:2nA:RH:RH:n3R:2nQ:H:n3R:RQ:RH:k:"))
