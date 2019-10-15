# 1.3

#%%
from secrets import token_bytes
from typing import Tuple


def random_key(length: int) -> int:
    tb: bytes = token_bytes(length)
    return int.from_bytes(tb, 'big')

print(random_key(5))


def encrypt(original:str) -> Tuple[int, int]:
    original_bytes: bytes = original.encode()
    dummy: int = random_key(len(original_bytes))
    original_key: int = int.from_bytes(original_bytes, 'big')
    encrypted: int = original_key ^ dummy
    return dummy, encrypted

encrypted_result = encrypt('One Time Pad!')
print(encrypted_result)


def decrypt(key1: int, key2: int) -> str:
    decrypted:int = key1 ^ key2
    temp: bytes = decrypted.to_bytes((decrypted.bit_length() +7) // 8, 'big')
    return temp.decode()

print(decrypt(*encrypted_result))


#%%
