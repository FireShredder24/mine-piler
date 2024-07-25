// To translate TISC-41 Assembly into Bytecode
//
// TISC-41 is a redstone computer by John Nguyen
// knightofthealtar64@gmail.com
// 24 July 2024

import java.util.Map;
import java.util.HashMap;
import java.util.Arrays;
import java.io.File;
import java.util.Scanner;
import java.io.FileNotFoundException;

public class BytecodeAssembler {
	private byte[] bytecode = new byte[256];
	private HashMap<String, Byte> opcodeMap = new HashMap<String, Byte>(); 
	

	public BytecodeAssembler() {
		// Binding instruction keywords to opcodes
		opcodeMap.put("ldi", (byte)0b00000000);
		opcodeMap.put("add", (byte)0b01000000);
		/*
		opcodeMap.put("sub", "10");
		opcodeMap.put("biz", "11");
		*/
	}

	public int parse(String filename) {
		try {	
			File asm = new File(filename);
			Scanner myReader = new Scanner(asm);
		        while (myReader.hasNextLine()) {
				byte instructionWord = 00000000;
				String data = myReader.nextLine();
				System.out.println(data);
		        }	
			myReader.close();
			return 0;
		} catch (FileNotFoundException e) {
			System.out.println("Cannot read file at " + filename);
			e.printStackTrace();
			return 1;
		}	
	}

	public static void main(String[] args) {
		BytecodeAssembler tiscAssembler = new BytecodeAssembler();
		tiscAssembler.parse("foo.asm");
	}
}
