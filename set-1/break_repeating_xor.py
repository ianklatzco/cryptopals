
from itertools import cycle

### 1-5 ###

def repeating_key_xor(plaintext: bytes, key: bytes):
	cyc = cycle(key)

	build = bytearray()
	for m,key in zip(plaintext, cyc):
		build.append(m ^ key)

	return build

### end 1-5 ###

with open('6.txt') as f:
	pass


KEYSIZE = 2 # up to 40. this is the length we are guessing for the key.

def compute_edit_distance(s1, s2):
	'''
	just the difference between the bits.
	i'm writing it for strings.
	'''

	# for each byte in the strings,
	# count the number of bits that are different.
	# is this just xor? xor then count the 1s?

	build = 0
	for b1, b2 in zip(s1,s2):
		build += bin(b1 ^ b2)[2:].count('1')


	return build


# For each KEYSIZE, take the first KEYSIZE worth of bytes, 
# and the second KEYSIZE worth of bytes, and find the edit 
# distance between them. Normalize this result by dividing by KEYSIZE.

#	take two blocks (at your given keysize)
#	compute edit distance and divide by KEYSIZE to normalize
#	the smallest one is your key, probably. grab the first three just in case.

# The KEYSIZE with the smallest normalized edit distance is probably
# the key. You could proceed perhaps with the smallest 2-3 KEYSIZE
# values. Or take 4 KEYSIZE blocks instead of 2 and average the distances.

# Now that you probably know the KEYSIZE: break the ciphertext into blocks of KEYSIZE length.
# Now transpose the blocks: make a block that is the first byte of every block, and a block that is the second byte of every block, and so on.
# Solve each block as if it was single-character XOR. You already have code to do this.
# For each block, the single-byte XOR key that produces the best looking histogram is the repeating-key XOR key byte for that block. Put them together and you have the key.


# broadly, there's two steps: find the KEYSIZE, then find the .... alignment, most likely, since it's probably a repeating key.