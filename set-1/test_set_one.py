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

def test_find_single_byte_xor_key():
	ciphertext = bytes.fromhex('1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736')
	find_single_byte_xor_key(ciphertext)
	pass

def test_decrypt_xor_d_message():
	ciphertext = bytes.fromhex('1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736')
	plaintext = b"Cooking MC\'s like a pound of bacon"

	key = find_single_byte_xor_key(ciphertext)

	r = decrypt_xor_d_message(ciphertext,88) # hardcoded lol

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
