from hex_to_b64 import *
import base64

def test(): 
	bytestring = bytes.fromhex('49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d')
	b64_string = bytes('SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t', 'ascii')

	assert hex_to_b64(bytestring) == b64_string

def test2():
	canonical = base64.b64encode(bytes('foobarbaz','ascii'))
	mine = hex_to_b64(bytearray('foobarbaz','ascii'))


# r = test1()

# print(r)
# print(type(r))
# print(r.decode('ascii'))