from pwn import *

byte_table=[0x0BB,0x2,0x9B,0x3,0x0C4,0x4,0x6C,0x5,0x4A,0x6,0x2E,0x7,0x22,
0x8,0x45,0x9,0x33,0x0A,0x0B8,0x0B,0x0D5,0x0C,0x6,0x0D,0x0A,
0x0E,0x0BC,0x0F,0x0FA,0x10,0x79,0x11,0x24,0x12,0x0E1,
0x13,0x0B2,0x14,0x0BF,0x15,0x2C,0x16,0x0AD,0x17,0x86,
0x18,0x60,0x19,0x0A4,0x1A,0x0B6,0x1B,0x0D8,0x1C,0x59,
0x1D,0x87,0x1E,0x41,0x1F,0x94,0x20,0x77,0x21,0x0F0,0x22,
0x4F,0x23,0x0CB,0x24,0x61,0x2,0x25,0x26,0x0C0,0x27,
0x97,0x28,0x2A,0x29,0x5C,0x2A,0x8,0x2B,0x0C9,0x2C,0x9F,
0x2D,0x43,0x2E,0x4E,0x2F,0x0CF,0x30,0x0F9,0x31,0x3E,
0x32,0x6F,0x33,0x65,0x34,0x0E7,0x35,0x0C5,0x36,0x39,
0x37,0x0B7,0x38,0x0EF,0x39,0x0D0,0x3A,0x0C8,0x3B,0x2F,
0x3C,0x0AA,0x3D,0x0C7,0x3E,0x47,0x3F,0x3C,0x40,0x81,
0x41,0x32,0x42,0x49,0x43,0x0D3,0x44,0x0A6,0x45,0x96,
0x46,0x2B,0x47,0x58,0x48,0x40,0x49,0x0F1,0x4A,0x9C,0x4B,
0x0EE,0x4C,0x1A,0x4D,0x5B,0x4E,0x0C6,0x4F,0x0D6,0x50,
0x80,0x51,0x2D,0x52,0x6D,0x53,0x9A,0x54,0x3D,0x55,0x0A7,
0x56,0x93,0x57,0x84,0x58,0x0E0,0x59,0x12,0x5A,0x3B,0x5B,
0x0B9,0x5C,0x9,0x5D,0x69,0x5E,0x0BA,0x5F,0x99,0x60,0x48,
0x61,0x73,0x62,0x0B1,0x63,0x7C,0x64,0x82,0x65,0x0BE,
0x66,0x27,0x67,0x9D,0x68,0x0FB,0x69,0x67,0x6A,0x7E,0x6B,
0x0F4,0x6C,0x0B3,0x6D,0x5,0x6E,0x0C2,0x6F,0x5F,0x70,0x1B,
0x71,0x54,0x72,0x23,0x73,0x71,0x74,0x11,0x75,0x30,0x76,
0xD2,0x77,0x0A5,0x78,0x68,0x79,0x9E,0x7A,0x3F,0x7B,
0x0F5,0x7C,0x7A,0x7D,0x0CE,0x7E,0x0B,0x7F,0x0C,0x80,
0x85,0x81,0x0DE,0x82,0x63,0x83,0x5E,0x84,0x8E,0x85,0x0BD,
0x86,0x0FE,0x87,0x6A,0x88,0x0DA,0x89,0x26,0x8A,0x88,
0x8B,0x0E8,0x8C,0x0AC,0x8D,0x3,0x8E,0x62,0x8F,0x0A8,0x90,
0x0F6,0x91,0x0F7,0x92,0x75,0x93,0x6B,0x94,0x0C3,0x95,
0x46,0x96,0x51,0x97,0x0E6,0x98,0x8F,0x99,0x28,0x9A,0x76,
0x9B,0x5A,0x9C,0x91,0x9D,0x0EC,0x9E,0x1F,0x9F,0x44,0x0A0,
0x52,0x0A1,0x1,0x0A2,0x0FC,0x0A3,0x8B,0x0A4,0x3A,0x0A5,
0x0A1,0x0A6,0x0A3,0x0A7,0x16,0x0A8,0x10,0x0A9,0x14,0x0AA,
0x50,0x0AB,0x0CA,0x0AC,0x95,0x0AD,0x92,0x0AE,0x4B,0x0AF,
0x35,0x0B0,0x0E,0x0B1,0x0B5,0x0B2,0x20,0x0B3,0x1D,0x0B4,
0x5D,0x0B5,0x0C1,0x0B6,0x0E2,0x0B7,0x6E,0x0B8,0x0F,0x0B9,
0x0ED,0x0BA,0x90,0x0BB,0x0D4,0x0BC,0x0D9,0x0BD,0x42,
0x0BE,0x0DD,0x0BF,0x98,0x0C0,0x57,0x0C1,0x37,0x0C2,0x19,
0x0C3,0x78,0x0C4,0x56,0x0C5,0x0AF,0x0C6,0x74,0x0C7,0x0D1,
0x0C8,0x4,0x0C9,0x29,0x0CA,0x55,0x0CB,0x0E5,0x0CC,0x4C,
0x0CD,0x0A0,0x0CE,0x0F2,0x0CF,0x89,0x0D0,0x0DB,0x0D1,
0x0E4,0x0D2,0x38,0x0D3,0x83,0x0D4,0x0EA,0x0D5,0x17,0x0D6,
0x7,0x0D7,0x0DC,0x0D8,0x8C,0x0D9,0x8A,0x0DA,0x0B4,0x0DB,
0x7B,0x0DC,0x0E9,0x0DD,0x0FF,0x0DE,0x0EB,0x0DF,0x15,
0x0E0,0x0D,0x0E1,0x2,0x0E2,0x0A2,0x0E3,0x0F3,0x0E4,0x34,
0x0E5,0x0CC,0x0E6,0x18,0x0E7,0x0F8,0x0E8,0x13,0x0E9,
0x8D,0x0EA,0x7F,0x0EB,0x0AE,0x0EC,0x21,0x0ED,0x0E3,0x0EE,
0x0CD,0x0EF,0x4D,0x0F0,0x70,0x0F1,0x53,0x0F2,0x0FD,0x0F3,
0x0AB,0x0F4,0x72,0x0F5,0x64,0x0F6,0x1C,0x0F7,0x66,0x0F8,
0x0A9,0x0F9,0x0B0,0x0FA,0x1E,0x0FB,0x0D7,0x0FC,0x0DF,
0x0FD,0x36,0x0FE,0x7D,0x0FF]

output=[39, 179, 115, 157, 245, 17, 231, 177, 
179, 190, 153, 179, 249, 249, 244, 48, 
27, 113, 153, 115, 35, 101, 153, 177,
101, 17, 17, 190, 35, 153, 39, 249, 
35, 153, 5, 101, 206]

print 'array size ='+str(len(byte_table))

print 'output size ='+str(len(output))

#flag{t4ble_l00kups_ar3_b3tter_f0r_m3}


for i in range(len(output)):
	print str(i)+' th: '
	for j in range(len(byte_table)):

		if byte_table[j]==output[i]:
			if byte_table[j-1]<126 and byte_table[j-1]>33:

				print chr(byte_table[j-1])
