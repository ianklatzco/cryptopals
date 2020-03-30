from set_one import *
import base64

def test_hex_to_b64_one(): 
	bytestring = bytes.fromhex('49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d')
	b64_string = bytes('SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t', 'ascii')

	assert hex_to_b64(bytestring) == b64_string

def test_hex_to_b64_two():
	canonical = base64.b64encode(bytes('foobarbaz','ascii'))
	mine = hex_to_b64(bytearray('foobarbaz','ascii'))
	assert canonical == mine

def test_score():
	h = score(b'Burning \'em, if you ain\'t quick and nimble\nI go crazy when I hear a cymbal')

def test_transpose():
	l1 = [['a', 'd'], ['b', 'e'], ['c', 'f']]
	b1 = []
	for l in l1:
		b1.append(list(map(ord,l)))

	l2 = [['a', 'c', 'e'], ['b', 'd', 'f']]
	b2 = []
	for l in l2:
		b2.append(list(map(ord,l)))

	assert transpose(b'abcdef',3) == b1
	assert transpose(b'abcdef',2) == b2

def test_find_single_byte_xor_key():
	ciphertext = bytes.fromhex('1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736')
	assert 88 == find_single_byte_xor_key(ciphertext)

	ciphertext = bytearray(b'(\n\n\x06\x1b\r\x00\x07\x0eI\x1d\x06I\x08\x05\x05I\x02\x07\x06\x1e\x07I\x05\x08\x1e\x1aI\x06\x0fI\x08\x1f\x00\x08\x1d\x00\x06\x07EI\x1d\x01\x0c\x1b\x0cI\x00\x1aI\x07\x06I\x1e\x08\x10I\x08I\x0b\x0c\x0cI\x1a\x01\x06\x1c\x05\rI\x0b\x0cI\x08\x0b\x05\x0cI\x1d\x06I\x0f\x05\x10GI \x1d\x1aI\x1e\x00\x07\x0e\x1aI\x08\x1b\x0cI\x1d\x06\x06I\x1a\x04\x08\x05\x05I\x1d\x06I\x0e\x0c\x1dI\x00\x1d\x1aI\x0f\x08\x1dI\x05\x00\x1d\x1d\x05\x0cI\x0b\x06\r\x10I\x06\x0f\x0fI\x1d\x01\x0cI\x0e\x1b\x06\x1c\x07\rGI=\x01\x0cI\x0b\x0c\x0cEI\x06\x0fI\n\x06\x1c\x1b\x1a\x0cEI\x0f\x05\x00\x0c\x1aI\x08\x07\x10\x1e\x08\x10I\x0b\x0c\n\x08\x1c\x1a\x0cI\x0b\x0c\x0c\x1aI\r\x06\x07N\x1dI\n\x08\x1b\x0cI\x1e\x01\x08\x1dI\x01\x1c\x04\x08\x07\x1aI\x1d\x01\x00\x07\x02I\x00\x1aI\x00\x04\x19\x06\x1a\x1a\x00\x0b\x05\x0cG')
	plaintext = b"According to all known laws of aviation, there is no way a bee should be able to fly. Its wings are too small to get its fat little body off the ground. The bee, of course, flies anyway because bees don't care what humans think is impossible."
	known_key = 0x69

	assert find_single_byte_xor_key(ciphertext) == known_key

def test_single_byte_xor():
	ciphertext = bytes.fromhex('1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736')
	plaintext = b"Cooking MC\'s like a pound of bacon"

	key = find_single_byte_xor_key(ciphertext)

	assert plaintext == single_byte_xor(ciphertext,key)


def test_xor_two_buffers():
	b1 = bytes.fromhex('1c0111001f010100061a024b53535009181c')
	b2 = bytes.fromhex('686974207468652062756c6c277320657965')

	res = bytes.fromhex('746865206b696420646f6e277420706c6179')

	assert xor_two_buffers(b1,b2) == res

def test_repeating_key_xor():
	plaintext = bytes('Burning \'em, if you ain\'t quick and nimble\nI go crazy when I hear a cymbal','ascii')
	key = bytes('ICE','ascii')

	goal_ciphertext = bytes.fromhex('0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f')

	assert repeating_key_xor(plaintext, key) == goal_ciphertext

def test_compute_edit_distance():
	assert 37 == compute_edit_distance(b'this is a test', b'wokka wokka!!!')

def test_break_repeating_xor():
	# assert break_repeating_xor() == False
	pass

def test_key_for_repeated_xor():
	ciphertext = open_file()

	key = [110, 32, 110, 32, 110]

	print(repeating_key_xor(ciphertext, key))
	# assert False
