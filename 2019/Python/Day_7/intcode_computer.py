import os
import copy


def get_program(filepath):
    # Load the comma separated intcode program from a file into memory (a list).
    with open(filepath) as f:
        incode = [int(v) for v in f.readline().split(",")]
    return incode


READ_PARAM = 0
WRITE_PARAM = 1


class IntCodeComputer:

    @staticmethod
    def restore_state(program, noun, verb):
        program[1] = noun
        program[2] = verb
        return program

    def run(self, program):
        self.program = program
        self.running = True
        self.instruction_pointer = 0
        self.next_instruction_pointer = None
        while self.running:
            opcode = self.program[self.instruction_pointer]
            method, input_modes = self.get_method(opcode)
            inputs = self.get_inputs(input_modes)
            self.perform_operation(method, inputs)
            self.increment_program_counter(inputs)
        return self.program

    def add(self, x, y, store_pos):
        self.program[store_pos] = x + y

    def multiply(self, x, y, store_pos):
        self.program[store_pos] = x * y

    def input(self, store_pos):
        self.program[store_pos] = int(input("Input:"))

    def output(self, value):
        print(value)

    def jump_if_true(self, test, value):
        if test:
            self.next_instruction_pointer = value

    def jump_if_false(self, test, value):
        self.jump_if_true(not test, value)

    def less_than(self, x, y, store_pos):
        if x < y:
            self.program[store_pos] = 1
        else:
            self.program[store_pos] = 0

    def equals(self, x, y, store_pos):
        if x == y:
            self.program[store_pos] = 1
        else:
            self.program[store_pos] = 0

    def halt(self):
        self.running = False

    def get_method(self, opcode):
        ops = {
            1: (self.add, [READ_PARAM, READ_PARAM, WRITE_PARAM]),
            2: (self.multiply, [READ_PARAM, READ_PARAM, WRITE_PARAM]),
            3: (self.input, [WRITE_PARAM]),
            4: (self.output, [READ_PARAM]),
            5: (self.jump_if_true, [READ_PARAM, READ_PARAM]),
            6: (self.jump_if_false, [READ_PARAM, READ_PARAM]),
            7: (self.less_than, [READ_PARAM, READ_PARAM, WRITE_PARAM]),
            8: (self.equals, [READ_PARAM, READ_PARAM, WRITE_PARAM]),
            99: (self.halt, []),
        }
        # Work with strings for this parsing because it's easier.
        opstring = str(opcode)
        code = int(opstring[-2:])
        method, args = ops[code]
        opstring = opstring[-3::-1]
        input_modes = []
        for i, arg in enumerate(args):
            if i + 1 > len(opstring):
                # Default if not given
                input_modes.append((0, arg))
            else:
                input_modes.append((int(opstring[i]), arg))
        return method, input_modes

    def get_inputs(self, input_modes):
        codes = []
        inputs = []
        for i, arg in enumerate(input_modes, start=self.instruction_pointer + 1):
            mode, arg_type = arg
            codes.append(self.program[i])
            if mode == 0:
                address = self.program[i]
                if arg_type == READ_PARAM:
                    inputs.append(self.program[address])
                elif arg_type == WRITE_PARAM:
                    inputs.append(address)
                else:
                    raise ValueError("Invalid parameter type {} for mode {}".format(arg_type, mode))
            elif mode == 1:
                if arg_type == READ_PARAM:
                    inputs.append(self.program[i])
                else:
                    raise ValueError("Invalid parameter type {} for mode {}".format(arg_type, mode))
            else:
                raise ValueError("Invalid Mode: {}".format(mode))
        return inputs

    def perform_operation(self, method, inputs):
        return method(*inputs)

    def increment_program_counter(self, inputs):
        if self.next_instruction_pointer is None:
            self.next_instruction_pointer = self.instruction_pointer + (1 + len(inputs))
        self.instruction_pointer = self.next_instruction_pointer
        self.next_instruction_pointer = None


def tests():
    computer = IntCodeComputer()

    assert computer.run([1,9,10,3,2,3,11,0,99,30,40,50])[0] == 3500
    assert computer.run([1,0,0,0,99,0,0,0]) == [2,0,0,0,99,0,0,0]
    assert computer.run([2,3,0,3,99,0,0,0]) == [2,3,0,6,99,0,0,0]
    assert computer.run([2,4,4,5,99,0,0,0]) == [2,4,4,5,99,9801,0,0]
    assert computer.run([1,1,1,4,99,5,6,0,99,0,0,0]) == [30,1,1,4,2,5,6,0,99,0,0,0]


if __name__ == "__main__":
    tests()

    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Input")
    program = get_program(input_file)

    computer = IntCodeComputer()
    computer.run(program)
