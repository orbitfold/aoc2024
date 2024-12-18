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
        pass

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
                    

@click.command()
@click.option('-i', '--input-file', help='Input data file')
def main(input_file):
    with open(input_file, 'r') as fd:
        data = fd.read()
        registers, program = data.split('\n\n')
        registers = [int(register[12:]) for register in registers.strip().split('\n')]
        program = [int(c) for c in program[9:].strip().split(',')]
        machine = Computer(a=registers[0], b=registers[1], c=registers[2])
        print(f"a:{machine.a}, b:{machine.b}, c:{machine.c}")
        print(program)
        machine.a = 200000
        machine.run(program)
        print(",".join([str(x) for x in machine.output]))
        
if __name__ == '__main__':
    main()
