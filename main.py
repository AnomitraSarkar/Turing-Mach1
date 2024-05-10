import os
import json

DEFAULT_FILENAME = "main.mach"

def read_mach(filename = DEFAULT_FILENAME):
    with open(filename) as f:
        code = f.read()
        return code

def process_code(filename):
    raw_code = read_mach(filename)
    split_code = raw_code.split(":")
    for i in range(0,len(split_code)):
        split_code[i] = split_code[i].split("\n")
        if(type(split_code)==list):
            try:
                split_code[i] = split_code[i].remove("")
            except:
                pass
    inline_code = []
    for i in split_code:
        if( i != None and i != []):
            for j in i:
                inline_code.append(j.strip())
    print(inline_code)
    
if __name__ == "__main__":
    process_code(DEFAULT_FILENAME)