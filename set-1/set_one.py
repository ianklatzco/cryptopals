from itertools import cycle
from collections import Counter
from functools import reduce
import base64
import operator
import string

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

def find_single_byte_xor_key_first_attempt(ciphertext):
	# look for highest-occurring character
	# assume it's e
	# e ^ highest freq = key

	e = Counter(ciphertext).most_common()

	# print(e)
	# print(list(map(lambda x: (hex(x[0]), x[1]),e)))

	key = e[0][0] ^ ord('e')

	# i'm kinda hairy, this doesn't work for our partic plaintext.
	# i don't really wanna design a more complex heuristic rn tho.

	# space is the highest-occuring char

	# so anyway, that approach is flawed. let's just find "percent of chars that are ascii-printable"

	return key

def find_single_byte_xor_key(ciphertext):
	list_of_all_keys = []
	for i in range(0,256):
		# xor i with everything in ciphertext
		xor = lambda x: x ^ i
		newlist = list(map(xor, ciphertext))

		list_of_all_keys.append(newlist)

	# list index corresponds to the xor key

	score_list = list(map(score, list_of_all_keys))
	# print(list(enumerate(score_list)))

	# find index of score_list's highest
	# warning that there could be multiple
	# maybe sort the list so the higher are @ the top?

	highest_score: Tuple = max(enumerate(score_list), key=lambda x: x[1])
	print(highest_score)
	# so the highest score is the list at this index, which means the index is our key.

	key = highest_score[0]
	return key

def score(text):

	# i wrote like four of these and no one of them worked consistently. see git history

	# for each character, grab its occurrence in the english alphabet from here
	# and add that to a total.

	# via wikipedia/Letter_frequency +
	# https://laconicwolf.com/2018/05/29/cryptopals-challenge-3-single-byte-xor-cipher-in-python/

	# the highest total represents the result most likely to be english text.
	scores = {'a':.08167, 'b':.01492, 'c':.02202, 'd':.04253, 'e':.12702, 'f':.02228, 
	 'g':.02015, 'h':.06094, 'i':.06966, 'j':.00153, 'k':.01292, 'l':.04025,
	 'm':.02406, 'n':.06749, 'o':.07507, 'p':.01929, 'q':.00095, 'r':.05987,
	 's':.06327, 't':.09356, 'u':.02758, 'v':.00978, 'w':.02560, 'x':.00150,
	 'y':.01994, 'z':.00077, ' ':.13}

	score = 0

	for byte in text:
		a = scores.get(chr(byte),0) # default 0
		score += a

	return score

def single_byte_xor(ciphertext,key):
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

def compute_edit_distance(b1, b2):
	'''
	just the difference between the bits.
	'''

	# for each byte in the strings,
	# count the number of bits that are different.
	# xor them and then count the ones.

	# map
	# xored = xor_two_buffers(b1, b2)
	# count_ones = lambda byte: bin(byte)[2:].count('1')
	# num_ones = sum(map(count_ones, xored))
	# return num_ones

	# filter (reduce)
	# xored = xor_two_buffers(b1, b2)
	# count_ones = lambda acc, byte: bin(byte)[2:].count('1') + acc
	# num_ones = reduce(count_ones, xored, 0)
	# return num_ones

	# for loop (string counting)
	# build = 0
	# for a, b in zip(b1,b2):
	# 	build += bin(a ^ b)[2:].count('1')
	# return build

	# for loop with bitshifts
	build = 0
	for byte in xor_two_buffers(b1,b2):
		for i in range(8):
			build += byte & 0x01
			byte >>= 1

	return build

def open_file():
	with open('6.txt') as f:
		c = f.readlines()
		b64 = ''.join(list(map(str.strip, c)))
		return base64.b64decode(b64)

def transpose(buf: bytes, keysize):
	b = []
	num_blocks = len(buf) // keysize

	for x in range(keysize):
		curr_b = []
		for block_index in range(num_blocks):
			e = buf[block_index * keysize + x]
			curr_b.append(e)
		b.append(curr_b)
	return b

def break_repeating_xor():

# For each KEYSIZE, take the first KEYSIZE worth of bytes, 
# and the second KEYSIZE worth of bytes, and find the edit 
# distance between them. Normalize this result by dividing by KEYSIZE.

#	take two blocks (at your given keysize)
#	compute edit distance and divide by KEYSIZE to normalize
#	the smallest one is your key, probably. grab the first three just in case.

# The KEYSIZE with the smallest normalized edit distance is probably
# the key. You could proceed perhaps with the smallest 2-3 KEYSIZE
# values. Or take 4 KEYSIZE blocks instead of 2 and average the distances.

	raw_bytes = open_file()

	list_of_normalized_edit_distances = [] # [(keysize, dist)]
	for keysize in range(2,41):
		first_block = raw_bytes[0:keysize]
		second_block = raw_bytes[keysize:2*keysize]
		h = compute_edit_distance(first_block, second_block)
		normalized_edit_distance = h / keysize

		list_of_normalized_edit_distances.append((keysize, normalized_edit_distance))

	# print(list_of_normalized_edit_distances)

	probable_keysize = min(list_of_normalized_edit_distances, key=lambda t: t[1])[0]
	list_of_normalized_edit_distances.remove((5,1.2))

	second_prob_keysize = min(list_of_normalized_edit_distances, key=lambda t: t[1])[0]
	list_of_normalized_edit_distances.remove((3,2.0))

	third_probable_keysize = min(list_of_normalized_edit_distances, key=lambda t: t[1])[0]

# Now that you probably know the KEYSIZE: break the ciphertext into blocks of KEYSIZE length.
# Now transpose the blocks: make a block that is the first byte of every block, and a block that is the second byte of every block, and so on.
# Solve each block as if it was single-character XOR. You already have code to do this.
# For each block, the single-byte XOR key that produces the best looking histogram is the repeating-key XOR key byte for that block. Put them together and you have the key.

	# tranpose blocks
	t = transpose(raw_bytes,probable_keysize)
	# print('ks1: ', probable_keysize)
	# print('ks2: ', second_prob_keysize)
	# print('ks3: ', third_probable_keysize)
	# now we have lists of ints that correspond to single-char xorable solves.

	# i want the keys for all of them.

	# print(t)
	key = list(map(find_single_byte_xor_key, t))

	return repeating_key_xor(raw_bytes, key)



# broadly, there's two steps: find the KEYSIZE, then find the .... alignment, most likely, since it's probably a repeating key.
# the approach for finding the alignment is interesting. naively i would probably iterate through each byte and decrypt a chunk, then
# manually check to see if that chunk is readable.

# but the approach they layout is slightly different. knowing the keysize, we first transpose the blocks so we get a bunch of containers 
# that hold the i'th byte or whatever. each of these has been xor'd with a single byte.

# oh! but it occurs to me that we don't know the key at all. getting the keysize alone is only part of the problem. we then need to recover the
# actual key, which is easiest to do with a single-key xor.