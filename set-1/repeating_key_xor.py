from itertools import cycle

def repeating_key_xor(plaintext: bytes, key: bytes):
	cyc = cycle(key)

	build = bytearray()
	for m,key in zip(plaintext, cyc):
		build.append(m ^ key)

	return build


