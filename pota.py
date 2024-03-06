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
        pro.append(F"cout <<{text};")

    elif opcode == 'read':
        text = line.replace("read", "")
        pro.append(F"cin >>{text};")

    elif opcode == 'if':
        pro.append(line)

    elif opcode == 'while':
        pro.append(line)

    elif opcode == 'try':
        function = True
        pro.append(opcode)
    
    elif opcode == 'except':
        function = True
        pro.append("catch () {")

    elif opcode == '{' or opcode == '}':
        pro.append(opcode)

    elif opcode == 'elif':
        text = line.replace("elif", "else if")
        pro.append(text)

    elif opcode == 'else' or opcode == 'else{':
        pro.append(line)

    elif opcode == 'var':
        text = line.replace("var ", "")
        pro.append(text + ";")


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
    elif opcode == 'use_cpp':
        module_name = line.replace("use_cpp ", "")
        modules.append(F"#include {module_name}")
    else:
        pro.append(line + ";")

    if function:
        program_func.extend(pro)
    else:
        program.extend(pro)

cpp_file = program_file[:-5] + ".cpp"
out = open(cpp_file, 'w')
out.write(f"#include <iostream>\n")
for i in modules:
    out.write(F"{i}\n")
out.write("using namespace std;\n")
for i in program_func:
    out.write(i)

out.write("int main(){")

for i in program:
    out.write(i)

out.write("return 0;}")
out.close()

os.system(F"g++ {cpp_file} -o main.exe")
# os.remove(cpp_file) # remove the '#' to delete the c++ source file aswell
