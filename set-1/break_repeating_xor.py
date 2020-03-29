from itertools import cycle
from collections import Counter

########## 1-1: convert hex to base64 ##########

# https://cryptopals.com/sets/1/challenges/1
# Always operate on raw bytes, never on encoded strings. Only use hex and base64 for pretty-printing.

# what does this mean?
# b'foo' instead of a regular s='foo'
#   we want to use the bytes or bytearray type in python, not the string type.
# indexing a str: returns char
# indexing a b'': returns int

# bytes() are immutable (b'')
# bytearray() are not.

# why does bytes require an encoding?
# no, each of these should correspond to a particular byte in the file.....
# i guess, if it's unicode, hm..... how would you interpret the four bytes or so?
# you'd need to specify the encoding.
ascii_rep = bytes('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=', 'ascii')
# each of these chars maps to a 6 bit value, starting at 000000 and up till 111111, incrementing as standard binary does.
# chunk 6 bits and do a table lookup.

# flatten = lambda l: [item for sublist in l for item in sublist]

def flatten(l):
	'''flattens doubly-nested lists.'''
	build = []
	for sublist in l:
		for item in sublist:
			build.append(item)
	return build

# TODO type annotations
def hex_to_b64(hex_as_raw_bytes):
	# padding
	if len(hex_as_raw_bytes) % 3 == 2:
		hex_as_raw_bytes.append(0x3D) # =
	elif len(hex_as_raw_bytes) % 3 == 1:
		hex_as_raw_bytes.append(0x3d)
		hex_as_raw_bytes.append(0x3d)

	# take 6 bits at a time
		# how to i grab 6 bits out of a bytearray?
		# nonconclusive answer.
		# guess i could look @ three at a time?
	# [] in hex_as_raw_bytes ¥
	three_at_a_time: list[bytearray] = \
		[ hex_as_raw_bytes[index:index+3] for index in range(0,len(hex_as_raw_bytes), 3) ]

	# [ bytearray(b'foo'), ...]

	list_24_bits_as_ascii = []
	for list_three_bytes in three_at_a_time:
		list_24_bits_as_ascii.append(''.join(list(map(lambda x: bin(x)[2::].zfill(8),list_three_bytes))))

	# print(list_24_bits_as_ascii)

	# [ strings of 24 bits ]
	list_6bits = []
	for bits in list_24_bits_as_ascii:
		# divide into groups of 6
		list_6bits.append( [ bits[i:i+6] for i in range(0,24,6) ] ) 

	# print(list_6bits)

	# [ 6bits, 6bits, 6bits, 6bits ]
	# this is a terrible way to write this code lol

	int_list = []
	for l in list_6bits:
		int_list.append( list(map(lambda x: int(x,2), l)) )
	# print(int_list)

	final_out = []

	for four_group in int_list:
		char_list = []
		for c in four_group:
			char_list.append(ascii_rep[c]) 
		final_out.append(char_list)
	# print(final_out)

	flat_list = flatten(final_out)

	b64 = ''.join(list(map(chr,flat_list)))

	return bytearray(b64,'ascii') # haha we are doing some type juggling here aren't we

	# yuck this is disgusting lmao

	# lookup: t[6bit]
	# add lookup result to building string

########## 1-2: xor two buffers ##########

def xor_two_buffers(b1, b2):
	build = bytearray()
	# b1 and b2 are equal length bytearray objects
	for a,b in zip(b1,b2):
		build.append(a ^ b)

	return build


########## 1-3: find a single-byte key ##########

# find the key, decrypt the message. what should our function return?
# probably guesses for the key, or the message.

def find_single_byte_xor_key(ciphertext):
	# look for highest-occurring character
	# assume it's e
	# e ^ highest freq = key

	e = Counter(ciphertext).most_common()

	# print(e)
	print(list(map(lambda x: (hex(x[0]), x[1]),e)))

	key = e[0][0] ^ ord('e')

	# i'm kinda hairy, this doesn't work for our partic plaintext.
	# i don't really wanna design a more complex heuristic rn tho.

	# space is the highest-occuring char

	return key

def decrypt_xor_d_message(ciphertext,key):
	build = bytearray()
	for c in ciphertext:
		build.append(c ^ key)
	return build

### 1-5: repeating-key xor ###

def repeating_key_xor(plaintext: bytes, key: bytes):
	'''eg key = ICE, repeating key is ICEICEICE'''
	cyc = cycle(key)

	ciphertext = xor_two_buffers(plaintext, cyc)

	return ciphertext

### 1-6: breaking repeating key xor ###

with open('6.txt') as f:
	pass


KEYSIZE = 2 # up to 40. this is the length we are guessing for the key.

def compute_edit_distance(b1, b2):
	'''
	just the difference between the bits.
	'''

	# for each byte in the strings,
	# count the number of bits that are different.
	# xor them and then count the ones.

	build = 0
	for a, b in zip(b1,b2):
		build += bin(a ^ b)[2:].count('1')

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
# the approach for finding the alignment is interesting. naively i would probably iterate through each byte and decrypt a chunk, then
# manually check to see if that chunk is readable.

# but the approach they layout is slightly different. knowing the keysize, we first transpose the blocks so we get a bunch of containers 
# that hold the i'th byte or whatever. each of these has been xor'd with a single byte.

# oh! but it occurs to me that we don't know the key at all. getting the keysize alone is only part of the problem. we then need to recover the
# actual key, which is easiest to do with a single-key xor.