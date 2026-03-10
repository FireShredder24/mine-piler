#!/usr/bin/python3

# Assembler for my 8-bit redstone computer architecture
# John Nguyen (c) 2026
# MIT License


import sys
import string

# Machine code is output with least significant bit on the LEFT.
# All comments must be prefixed a #
# No blank lines!

# First 4 bits are the opcode
# wwww is the first 4-bit argument (usually a register writeback address)
# aaaa is the second 4-bit argument (always a register read address)
# bbbb is the third 4-bit argument (always a register read address)
# dddddddd is the first (and only) 8-bit argument (an immediate value or instruction address)

# Real instruction matrix
real = {
	"ADD":"0000wwwwaaaabbbb",
	"SUB":"1000wwwwaaaabbbb",
	"LDI":"0100wwwwdddddddd",
	"OR":"1100wwwwaaaabbbb",
	"AND":"0010wwwwaaaabbbb",
	"NOR":"1010wwwwaaaabbbb",
	"NAND":"0110wwwwaaaabbbb",
	"BIZ":"1110wwwwdddddddd",
	"LOAD":"0001wwwwaaaa0000",
	"STOR":"10010000wwwwaaaa",
	"ORI":"0101wwwwdddddddd",
	"ANDI":"1101wwwwdddddddd",
	"NORI":"0011wwwwdddddddd",
	"NANDI":"1011wwwwdddddddd",
	"LODDS":"0111wwwwaaaa0000",
	"DRAW":"11110000wwwwaaaa"
}
# Implied no-operand instructions
impliedZero = {
	"NOOP":"0000000000000000"
}
# Implied one-operand instructions
impliedOne = {
	"JUMP":"11100000dddddddd"
}
# Implied two-operand instructions
impliedTwo = {
	"COPY":"0000wwwwaaaa0000",
	"NOT":"1010wwwwaaaaaaaa"
}


stripmask = string.ascii_letters+"!."
stripmask.replace("b","")

def assemble(line):
	words = line.split()
	count = len(words)
	assembly = "0000000000000000"
	template = {}

	if count > 4:
		print('too many arguments!')
		return 1

	# This strips the letters from tokens and converts to integers
	values = [0,0,0,0]
	for idx, token in enumerate(words):
		if idx != 0:
			try:
				token = token.strip(stripmask)
				# converts from binary if contains "b"
				if "b" in token:
					value = int(token.strip("b"),2) 
				# converts from base-10 otherwise
				else:
					value = int(token)
				values[idx] = value
			except:
				if ("JUMP" in words or "BIZ" in words) and idx == len(words)-1:
					values[idx] = 0
				else:
					print(f"Unexpected non-numeric token at index {idx}!")
					return 3

	# Figure out which template dictionary to search in
	if words[0] in real:
		template = real
	elif words[0] in impliedZero:
		template = impliedZero
	elif words[0] in impliedOne:
		template = impliedOne
	elif words[0] in impliedTwo:
		template = impliedTwo
	else:
		print(f'no template found for token {words[0]}')
		return 2

	assembly = template[words[0]] # grabs the instruction template from the specified mnemonic

	if count == 4:
		# Extract the 3 operands and convert them to binary strings
		wwww = format(values[1],'04b')[::-1]
		aaaa = format(values[2],'04b')[::-1]
		bbbb = format(values[3],'04b')[::-1]
		# Replace the fields in the template with the operands
		assembly = assembly.replace("wwww",wwww)
		assembly = assembly.replace("aaaa",aaaa)
		assembly = assembly.replace("bbbb",bbbb)
		# return the assembled line
		return assembly
	elif count == 3:
		if "dddddddd" in assembly:
			wwww = format(values[1],'04b')[::-1]
			assembly = assembly.replace("wwww",wwww)
			if not "!" in words[2]:		
				dddddddd = format(values[2],'08b')[::-1]
				assembly = assembly.replace("dddddddd",dddddddd)	
				return assembly
			else:
				return assembly+words[2].strip("!\n")
		else:
			wwww = format(values[1],'04b')[::-1]
			aaaa = format(values[2],'04b')[::-1]
			assembly = assembly.replace("wwww",wwww)
			assembly = assembly.replace("aaaa",aaaa)
			return assembly
	elif count == 2:
		if "dddddddd" in assembly:
			dddddddd = format(values[1],'08b')[::-1]
			assembly = assembly.replace("dddddddd",dddddddd)
			if not "!" in words[1]:		
				dddddddd = format(values[1],'08b')[::-1]
				assembly = assembly.replace("dddddddd",dddddddd)	
				return assembly
			else:
				return assembly+words[1].strip("!")
		else:
			wwww = format(values[1],'04b')[::-1]
			assembly = assembly.replace("wwww",wwww)
			return assembly
	else:
		return assembly


def file_assemble(path_in, path_out = ""):
	f = open(path_in,"rt")
	out = []
	inspointer = 0
	subroutines = {}
	for n, line in enumerate(f):
		# Strip comments from the end of the line
		while "#" in line:
			line = line[:-1]
		# If there's anything left it's either...
		if len(line) != 0:
			# A subroutine key
			if line[0] == ".":
				subroutines[line[1:].strip("\n")] = inspointer + 1 
			# Or an actual instruction
			else: 
				inspointer = inspointer + 1
				assembly = assemble(line)
				# if it's less than 16 characters it's an error code
				if type(assembly) == int:
					print(f"Assembler exited with error code {assembly} at line {n+1}")
					exit() 
				# if it's longer than 16 characters then we have a subroutine key included
				if len(assembly) > 16:
					final = assembly[0:16] # the machine code template
					key = assembly[16:]
					try:
						pointer = subroutines[key]
					except:
						print(f'Key {key} not found in subroutines {subroutines}')
						exit()
					pointerstr = format(int(pointer),'08b')[::-1]
					final = final.replace("dddddddd",pointerstr)
				else:
					final = assembly
				out.append(final)
		
	if path_out != "":
		outf = open(path_out,"wt")
		for line in out:
			outf.write(line)
			outf.write("\n")
	else:
		print(out)

if __name__ == '__main__':
	pathi = sys.argv[1]
	if len(sys.argv) > 2: 
		patho = sys.argv[2]
		file_assemble(pathi,patho)
	elif len(sys.argv) == 2:
		file_assemble(pathi)
	else:
		print("Too few arguments!")
