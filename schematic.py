#!/usr/bin/env python

# this script takes bytecode in leftmost LSB
# for my minecraft redstone computer
# and converts it into a schematic that can be pasted
# into the instruction ROM.

import mcschematic
import sys

datablocks = {
	"0":"minecraft:black_wool",
	"1":"minecraft:repeater[facing=north]"
}

def schematic(pathi, patho = ""):
	try:
		bytecode = open(pathi,"rt")
	except:
		print("Failed to open input bytecode file!")
		exit()
	schem = mcschematic.MCSchematic()
	for idx, line in enumerate(bytecode):
		line = line.strip("\n")
		z = int(idx / 16) * (-7) # Rows are distributed on Z axis every 16
		x = int(idx % 16) * (-2) # Spacing is 2 along the negative X
		if type(line) == str and len(line) == 16:
			y = 0
			for pos, char in enumerate(line):
				try:
					block = datablocks[char]
				except:
					print(f"Failed to extract block from {char} of type {type(char)} at index {pos} in line {idx}") 
					exit()
				coords = (x, y, z)
				schem.setBlock(coords, block) # setting the data block
				y = y+2
	if patho == "":
		patho = pathi[:-3]
	schem.save("schematics",patho,mcschematic.Version.JE_1_20_1)

if __name__ == "__main__":
	args = sys.argv
	if len(args) < 2:
		print("Too few arguments! needs an input file path")
	elif len(args) > 3:
		print("Too many arguments! wtf")
	else:
		pathi = args[1]
		patho = ""
		if len(args) == 3:
			patho = args[2]
		schematic(pathi, patho)

