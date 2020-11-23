"""
the file could process strings like

Disassembly of section .text:

00000698 <__atexit_handler_wrapper>:
     698:	e3500000 	cmp	r0, #0
     69c:	012fff1e 	bxeq	lr
     6a0:	e12fff10 	bx	r0

000006a4 <_start>:
     6a4:	e59fc05c 	ldr	ip, [pc, #92]	; 708 <_start+0x64>
     6a8:	e59f205c 	ldr	r2, [pc, #92]	; 70c <_start+0x68>
     6ac:	e92d4800 	push	{fp, lr}
     6b0:	e08fc00c 	add	ip, pc, ip
     6b4:	e28db004 	add	fp, sp, #4
     6b8:	e59f3050 	ldr	r3, [pc, #80]	; 710 <_start+0x6c>
     6bc:	e24dd010 	sub	sp, sp, #16
     6c0:	e59f104c 	ldr	r1, [pc, #76]	; 714 <_start+0x70>
     6c4:	e79c2002 	ldr	r2, [ip, r2]
     6c8:	e50b2014 	str	r2, [fp, #-20]	; 0xffffffec
     6cc:	e59f2044 	ldr	r2, [pc, #68]	; 718 <_start+0x74> 
"""

import re
import argparse
parser = argparse.ArgumentParser()
parser.description='please enter one parameters filename'
parser.add_argument("-i",  help="this is a filename", dest="filename", type=str, default="0")

args = parser.parse_args()
filename = args.filename
rule = re.compile(r' {1,2}(?P<address>[\dabcdef]+:)	(?P<assem_bin>[\dabcdef]+)(?P<tab> *\t)(?P<assem_dis>(.*))')
start_address_rule = re.compile(r'<\w+>')

filename = args.filename
#print(type(filename))
if filename == "0":
	print("Use -h to view args")
	exit()
file = filename
fr  = open(file,'r')
res_list = []
data = fr.readline()
while data:
	address = None
	if "Disassembly of section" in data or '\t...\n' == data or len(data)==1 or "file format elf64-x86-64" in data:
		data = fr.readline()
		continue
	data = data.strip('\n')
	#print(data)
	res = re.search(rule,data)
	#print(res)
	if res:
		address,assem_bin,assem_dis = res.group("address"),res.group("assem_bin"),res.group("assem_dis")
		address = re.sub(r':',';',address)
		assem_bin += ';'
		print(address[-4:],assem_bin,assem_dis)
		res_list.append(address[-4:] + assem_bin + assem_dis)
	else:
		res_list.append(data)
	data = fr.readline()
reverse_res = res_list[::-1]
fw = open(file+'_bak','w')
for _ in reverse_res:
	fw.write(_+"\n")
fw.close()
