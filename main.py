import os

DEFAULT_FILENAME = "main.mach"

def read_mach(filename = DEFAULT_FILENAME):
    with open(filename) as f:
        code = f.read()
        return code
    

    
if __name__ == "__main__":
    read_mach()