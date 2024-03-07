import sys
import os
import re

def load_module(module_name):
    module_file = module_name + ".pota"
    with open(module_file, "r") as f:
        return f.readlines()

if len(sys.argv) != 2:
    print("Useage:> pota <filename>.pota")
    sys.exit()
else:
    program_file = sys.argv[1]

program_lines = []
with open(program_file, "r") as f:
    program_lines = [line.strip() for line in f.readlines()]

program = []
program_func = []
modules = []
function = False
for line in program_lines:
    parts = line.split(" ")
    opcode = parts[0]
    pro = []
    if opcode == " ":
        continue

    elif opcode == 'print':
        text = line.replace("print", "")
        pro.append(F"fmt.Printf({text})")

    elif opcode == 'read':
        text = line.replace("read", "")
        pro.append(F"fmt.Scan({text})")

    elif opcode == 'if':
        pro.append(line)

    elif opcode == 'while':
        pro.append(line)

    elif opcode == 'foreach':
        text = line.replace("in", ":=")
        pro.append(text)

    elif opcode == 'for':
        pro.append(line)

    elif opcode == 'try {':
        function = True
        pro.append("try := func() {")
    
    elif opcode == 'error':
        pro.append("return nil")
        function = True
        pro.append("if err := try(); err != nil{")

    elif opcode == '{' or opcode == '}':
        pro.append(opcode)

    elif opcode == 'elif':
        text = line.replace("elif", "else if")
        pro.append(text)

    elif opcode == 'else' or opcode == 'else{':
        pro.append(line)

    elif opcode == 'var':
        text = line.replace("=", ":=")
        pro.append(text)


    elif opcode == 'func':
        function = True
        text = line.replace("func ", line.rsplit("-> ")[1].replace(" {", " "))
        text = re.sub(r"->.*{$", "{", text)
        pro.append(text)

    elif opcode == '}!':
        pro.append('}')
        program_func.extend(pro)
        function = False
        continue
    
    elif opcode == '#':
        continue

    elif opcode == 'ret':
        text = line.replace("ret", "")
        pro.append(F"return{text};")

    elif opcode == 'use':
        module_name = line.replace("use ", "")
        program_lines = program_lines.extend([line.strip() for line in load_module(module_name)])
    elif opcode == 'use_go':
        module_name = line.replace("use_go ", "")
        modules.append(module_name)
    else:
        pro.append(line + ";")

    if function:
        program_func.extend(pro)
    else:
        program.extend(pro)

go_file = program_file[:-5] + ".go"
os.system(f"go mod init {program_file[:-5]}")
out = open(go_file, 'w')
out.write(f"package main\nimport(\n\"fmt\"")
for i in modules:
    out.write(F"\"{i}\"\n")
out.write(f"\n)\n")

for i in program_func:
    out.write(i)

out.write("func main(){")

for i in program:
    out.write(f"\"{i}\"")

out.write("}")
out.close()

os.system(F"go build -o {go_file}.exe")
# os.remove(go_file)
