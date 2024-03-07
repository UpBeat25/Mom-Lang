import sys
import os

def load_module(module_name):
    module_file = module_name + ".pota"
    with open(module_file, "r") as f:
        return f.readlines()

build = False
if len(sys.argv) != 2:
    print("Usage:> pota <filename>.pota")
    sys.exit()
else:
    if sys.argv[1] == 'install':
        pass
    elif sys.argv[1] == 'build':
        build = True
        program_file = sys.argv[2]
    else:
        program_file = sys.argv[1]

program_lines = []
with open(program_file, "r") as f:
    program_lines = [line.strip() for line in f.readlines()]

program = []
program_func = []
modules = []
function = False
try_number = 1
for line in program_lines:
    parts = line.split(" ")
    opcode = parts[0]
    pro = []
    if opcode == " ":
        continue

    elif opcode == 'print':
        text = line.replace("print ", "")
        pro.append(F"fmt.Println({text})")
    
    elif opcode == 'printf':
        text = line.replace("printf ", "")
        pro.append(F"fmt.Printf({text})")

    elif opcode == 'read':
        text = line.replace("read ", "")
        pro.append(F"fmt.Scan(&{text})")

    elif opcode == 'if':
        pro.append(line)

    elif opcode == 'while':
        pro.append(line)

    elif opcode == 'foreach':
        text = line.replace("in", ":=")
        pro.append(text)

    elif opcode == 'for':
        pro.append(line)

    elif opcode == 'try':
        pro.append(F"try{try_number} := func() error" + "{")
    
    elif opcode == 'catch':
        pro.append(F"if err := try{try_number}(); err != nil" + "{")
        try_number += 1

    elif opcode == 'elif':
        text = line.replace("elif", "else if")
        pro.append(text)

    elif opcode == 'var':
        text = line.replace("=", ":=").replace("var ", "")
        pro.append(text)

    elif opcode == 'let':
        text = line.replace("let", "var")
        pro.append(text)

    elif opcode == 'func':
        text = line.replace("->", "")
        function = True
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
        pro.append(line)

    if function:
        program_func.extend(pro)
    else:
        program.extend(pro)

go_file = program_file[:-5] + ".go"
if not os.path.exists("go.mod"):
    os.system(f"go mod init {program_file[:-5]}")
out = open(go_file, 'w')
out.write(f"package {program_file[:-5]}\nimport(\n\"fmt\"\n")
for i in modules:
    out.write(F"\"{i}\"\n")
out.write(f"\n)\n")

for i in program_func:
    out.write(i + "\n")

out.write("func main(){")

for i in program:
    out.write(f"{i}\n")

out.write("}")
out.close()

if build is True:
    os.system(F"go build -o {program_file[:-5]}.exe")
    os.remove(go_file)
else:
    os.system(F"go run {go_file}")
