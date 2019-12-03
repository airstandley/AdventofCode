import os


def get_program(filepath):
    # Load the comma separated intcode program from a file into memory (a list).
    with open(filepath) as f:
        incode = [int(v) for v in f.readline().split(",")]
    return incode


def restore_state(program):
    program[1] = 12
    program[2] = 2
    return program


class IntCodeComputer:

    def run(self, program):
        self.program = program
        self.running = True
        self.program_counter = 0
        while self.running:
            opcode = self.program[self.program_counter]
            inputs = [self.program[self.program_counter + i] for i in range(1, 4)]
            self.perform_operation(opcode, inputs)
            self.program_counter += 4
        return self.program

    def add(self, inputs):
        x_pos, y_pos, store_pos = inputs
        self.program[store_pos] = self.program[x_pos] + self.program[y_pos]

    def multiply(self, inputs):
        x_pos, y_pos, store_pos = inputs
        self.program[store_pos] = self.program[x_pos] * self.program[y_pos]

    def halt(self, inputs):
        self.running = False

    def perform_operation(self, opcode, inputs):
        ops = {
            1: self.add,
            2: self.multiply,
            99: self.halt
        }
        ops[opcode](inputs)


if __name__ == "__main__":
    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Input")
    program = get_program(input_file)

    computer = IntCodeComputer()
    print(computer.run(restore_state(program))[0])


def tests():
    computer = IntCodeComputer()

    assert computer.run([1,9,10,3,2,3,11,0,99,30,40,50])[0] == 3500
    assert computer.run([1,0,0,0,99,0,0,0]) == [2,0,0,0,99,0,0,0]
    assert computer.run([2,3,0,3,99,0,0,0]) == [2,3,0,6,99,0,0,0]
    assert computer.run([2,4,4,5,99,0,0,0]) == [2,4,4,5,99,9801,0,0]
    assert computer.run([1,1,1,4,99,5,6,0,99,0,0,0]) == [30,1,1,4,2,5,6,0,99,0,0,0]