// This class is a template for the implementation of a single instruction

public class InstructionDef {
	protected String key;
	protected int argc;
	
	public InstructionDef(String key, int argc) {
		
	}

	public int getArgC() {
		return argc;
	}

	public String getKey() {
		return key;
	}


}
