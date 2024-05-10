import os
import json

DEFAULT_FILENAME = "main.mach"

class Machine:
    init = "q0"
    final="qf"
    transition=[]
    tapeStr = '_'
    tapeList = ["_"]
    
    def __init__(self,init,final,trans) -> None:
        self.init = init;
        self.final = final
        self.transition = trans
    
    def compile(self)->None:
       tapeInput = input("Enter Input String Load on Tape: ")
       self.tape = f"_{tapeInput}_"
       
    def concurrentRun(self)->str:
        self.tapeList = list(self.tapeStr)
        return "A"
        
       
    



def read_mach(filename = DEFAULT_FILENAME):
    with open(filename) as f:
        code = f.read()
        return code

def process_code(filename):
    raw_code = read_mach(filename)
    split_code = raw_code.split(":")
    for i in range(0,len(split_code)):
        split_code[i] = split_code[i].split("\n")
    for i in range(0,len(split_code)):
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