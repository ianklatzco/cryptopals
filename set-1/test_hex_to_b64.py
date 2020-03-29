from hex_to_b64 import *
import base64

def test1(): 
	bytestring = bytes.fromhex('49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d')
	b64_string = bytes('SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t', 'ascii')

	assert hex_to_b64(bytestring) == b64_string

def test2():
	canonical = base64.b64encode(bytes('foobarbaz','ascii'))
	mine = hex_to_b64(bytearray('foobarbaz','ascii'))
	assert canonical == mine

def test_xor_two_buffers():
	b1 = bytes.fromhex('1c0111001f010100061a024b53535009181c')
	b2 = bytes.fromhex('686974207468652062756c6c277320657965')

	res = bytes.fromhex('746865206b696420646f6e277420706c6179')

	assert xor_two_buffers(b1,b2) == res
