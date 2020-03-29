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
		build += bin(ord(b1) ^ ord(b2))[2:].count('1')


	return build

