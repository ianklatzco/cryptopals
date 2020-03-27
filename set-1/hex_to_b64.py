# convert hex to base64

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


r = hex_to_b64(bytearray('foobarbaz','ascii'))
# print('result: ', r)
