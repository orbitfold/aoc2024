import click

class Computer:
    def __init__(self, a=0, b=0, c=0):
        self.a = a
        self.b = b
        self.c = c
        self.pointer = 0
        self.output = []

    def combo(self, arg):
        if 0 <= arg <= 3:
            return arg
        elif arg == 4:
            return self.a
        elif arg == 5:
            return self.b
        elif arg == 6:
            return self.c
        else:
            raise RuntimeError

    def adv(self, arg):
        self.a = int(self.a / (2 ** self.combo(arg)))
        self.pointer += 2

    def bxl(self, arg):
        self.b = self.b ^ arg
        self.pointer += 2

    def bst(self, arg):
        self.b = self.combo(arg) % 8
        self.pointer += 2

    def jnz(self, arg):
        if self.a != 0:
            self.pointer = arg
        else:
            self.pointer += 2

    def bxc(self, arg):
        self.b = self.b ^ self.c
        self.pointer += 2

    def out(self, arg):
        self.output.append(self.combo(arg) % 8)
        self.pointer += 2
        
    def bdv(self, arg):
        self.b = int(self.a / (2 ** self.combo(arg)))
        self.pointer += 2

    def cdv(self, arg):
        self.c = int(self.a / (2 ** self.combo(arg)))
        self.pointer += 2

    def print_state(self):
        print(f"a: {self.a}, b: {self.b}, c: {self.c}, pointer: {self.pointer}")

    def disassemble(self, program):
        def parse_combo(arg):
            if 0 <= arg <= 3:
                return str(arg)
            elif arg == 4:
                return "a"
            elif arg == 5:
                return "b"
            elif arg == 6:
                return "c"
            else:
                raise RuntimeError
        for p in range(0, len(program), 2):
            opcode, arg = program[p], program[p + 1]
            if opcode == 0:
                print(f"adv {parse_combo(arg)}")
            elif opcode == 1:
                print(f"bxl {arg}")
            elif opcode == 2:
                print(f"bst {parse_combo(arg)}")
            elif opcode == 3:
                print(f"jnz {arg}")
            elif opcode == 4:
                print(f"bxc")
            elif opcode == 5:
                print(f"out {parse_combo(arg)}")
            elif opcode == 6:
                print(f"bdv {parse_combo(arg)}")
            elif opcode == 7:
                print(f"cdv {parse_combo(arg)}")

    def run(self, program, debug=False):
        self.pointer = 0
        while True:
            if program[self.pointer] == 0:
                self.adv(program[self.pointer + 1])
            elif program[self.pointer] == 1:
                self.bxl(program[self.pointer + 1])
            elif program[self.pointer] == 2:
                self.bst(program[self.pointer + 1])
            elif program[self.pointer] == 3:
                self.jnz(program[self.pointer + 1])
            elif program[self.pointer] == 4:
                self.bxc(program[self.pointer + 1])
            elif program[self.pointer] == 5:
                self.out(program[self.pointer + 1])
            elif program[self.pointer] == 6:
                self.bdv(program[self.pointer + 1])
            elif program[self.pointer] == 7:
                self.cdv(program[self.pointer + 1])
            else:
                raise RuntimeError
            if debug:
                self.print_state()
            if self.pointer >= len(program):
                break

def candidates(a0, output):
    result = []
    for offset in range(8):
        a = a0 + offset
        b = a % 8
        b = b ^ 1
        c = a // (2 ** b)
        b = b ^ c
        b = b ^ 4
        if b % 8 == output:
            result.append(a * 8)
    return result

def iterates(program):
    candidate_list = [0]
    for x in reversed(program):
        new_candidate_list = []
        for candidate in candidate_list:
            new_candidate_list += candidates(candidate, x)
        candidate_list = new_candidate_list
    return candidate_list
    
@click.command()
@click.option('-i', '--input-file', help='Input data file')
def main(input_file):
    with open(input_file, 'r') as fd:
        data = fd.read()
        registers, program = data.split('\n\n')
        registers = [int(register[12:]) for register in registers.strip().split('\n')]
        program = [int(c) for c in program[9:].strip().split(',')]
        print(program)
        machine = Computer(a=registers[0], b=registers[1], c=registers[2])
        machine.disassemble(program)
        machine.a = min(iterates(program)) // 8
        print(machine.a)
        machine.run(program)
        print(",".join([str(x) for x in machine.output]))
        
if __name__ == '__main__':
    main()
