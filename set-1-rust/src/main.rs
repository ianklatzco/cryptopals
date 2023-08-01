#![allow(dead_code)]
#![allow(unused_variables)]
#![allow(unused_imports)]
use base64::{Engine as _, engine::general_purpose};
use std::fs::File;
use std::io::Error;

fn main() {
	set1_1();
	set1_2();
	set1_3();
	set1_4();
}

fn fixed_length_xor(v1: Vec<u8>, v2: Vec<u8>) -> Vec<u8> {
	assert_eq!(v1.len(), v2.len());

	let mut retvec: Vec<u8> = Vec::new();

	for (e1, e2) in v1.iter().zip(v2.iter()) { // you can zip an iter?
		retvec.push(e1 ^ e2);
	}

	retvec
}

fn unhexlify(hex_string: &str) -> Vec<u8> {
	let mut bytes: Vec<u8> = Vec::new();
	for i in (0..hex_string.len()).step_by(2) {
		let hex_byte = &hex_string[i..(i+2)];
		if let Ok(byte) = u8::from_str_radix(hex_byte,16) {
			bytes.push(byte);
		} else {
			panic!("invalid hex input");
		}
	}
	bytes
}

fn hexlify(raw_bytes: Vec<u8>) -> String {
	raw_bytes.iter()
		.map(|byte| format!("{:02x}", byte))
		.collect()
}

fn b64encode(instr: Vec<u8>) -> String {
	general_purpose::STANDARD_NO_PAD.encode(instr)
}

fn b64decode(instr: Vec<u8>) -> Vec<u8> {
	general_purpose::STANDARD_NO_PAD.decode(instr).unwrap()
}

// -------------------------------------------------

fn set1_1() {
	let s1 = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d";
	let res = unhexlify(s1);
	let res1 = b64encode(res);
	// let res1 = general_purpose::STANDARD_NO_PAD.encode(res);
	assert_eq!(res1, String::from("SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t"));
}

fn set1_2() {
	let s1 = unhexlify("1c0111001f010100061a024b53535009181c");
	let s2 = unhexlify("686974207468652062756c6c277320657965");
	let r3 = hexlify(fixed_length_xor(s1,s2));
	assert_eq!(r3, "746865206b696420646f6e277420706c6179");
	// dbg!(r3);
}

fn set1_3() {
	let sss = unhexlify("1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736");
	let len = sss.len();
	/*
	let len = sss.len();
	for i in 0..256 {
		// dbg!(i);
		let vvv: Vec<u8>= vec![i as u8; len];
		let res = fixed_length_xor(sss.clone(), vvv); // vec![u8 of 3 of len 32]
		//println!("{:?}", &res);
		let ascii = String::from_utf8(res).expect("unprintable");
		dbg!(i); // 88 
		dbg!(ascii);
	}
	*/
	let outstr = fixed_length_xor(sss, vec![88 as u8; len]);
	assert_eq!(String::from_utf8(outstr).unwrap(), String::from("Cooking MC's like a pound of bacon"));
	// dbg!(outstr);
}

fn score() {
}

fn set1_4() {
	let file = File::open("4.txt")?;
	// each line contains hex-encoded string
}
