import os
import copy
import queue


def get_program(filepath):
    # Load the comma separated intcode program from a file into memory (a list).
    with open(filepath) as f:
        incode = [int(v) for v in f.readline().split(",")]
    return incode


READ_PARAM = 0
WRITE_PARAM = 1


class IntCodeComputer:
    debug = False

    def __init__(self, program, input_queue=None, output_queue=None, name="IntCodeComputer"):
        self.program = copy.copy(program)
        self.program_memory = None
        self.relative_base = None
        self.instruction_pointer = None
        self.next_instruction_pointer = None
        self.running = None
        self.input_queue = input_queue
        self.output_queue = output_queue
        self.name = name

    @staticmethod
    def restore_state(program, noun=None, verb=None):
        if noun is not None:
            program[1] = noun
        if verb is not None:
            program[2] = verb
        return program

    def run(self, noun=None, verb=None):
        self.program_memory = self.restore_state(copy.copy(self.program), noun, verb)
        self.relative_base = 0
        self.instruction_pointer = 0
        self.next_instruction_pointer = None
        self.running = True
        if self.debug:
            print("Program Start For", self.name)
        while self.running:
            opcode = self.program_memory[self.instruction_pointer]
            method, input_modes = self.get_method(opcode)
            inputs = self.get_inputs(input_modes)
            if self.debug:
                print("Instruction:{}({}) Inputs:{}({})".format(opcode, method.__name__, inputs, input_modes))
            self.perform_operation(method, inputs)
            self.increment_program_counter(inputs)
        return self.program_memory

    def add(self, x, y, store):
        self.program_memory[store] = self.program_memory[x] + self.program_memory[y]

    def multiply(self, x, y, store):
        self.program_memory[store] = self.program_memory[x] * self.program_memory[y]

    def input(self, store):
        if self.input_queue is None:
            value = int(input("Input:"))
        elif hasattr(self.input_queue, 'get'):
            value = self.input_queue.get()
        elif hasattr(self.input_queue, 'pop'):
            value = self.input_queue.pop(0)
        else:
            raise RuntimeError("Invalid input configured.")

        self.program_memory[store] = value

    def output(self, address):
        value = self.program_memory[address]
        if self.output_queue is None:
            print(value)
        elif hasattr(self.output_queue, 'push'):
            self.output_queue.push(value)
        elif hasattr(self.output_queue, 'append'):
            self.output_queue.append(value)
        else:
            raise RuntimeError("Invalid output configured.")

    def jump_if_true(self, test, jump):
        if self.program_memory[test]:
            self.next_instruction_pointer = self.program_memory[jump]

    def jump_if_false(self, test, jump):
        if not self.program_memory[test]:
            self.next_instruction_pointer = self.program_memory[jump]

    def less_than(self, x, y, store):
        if self.program_memory[x] < self.program_memory[y]:
            self.program_memory[store] = 1
        else:
            self.program_memory[store] = 0

    def equals(self, x, y, store):
        if self.program_memory[x] == self.program_memory[y]:
            self.program_memory[store] = 1
        else:
            self.program_memory[store] = 0

    def adjust_relative_offset(self, address):
        value = self.program_memory[address]
        self.relative_base += value

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
            9: (self.adjust_relative_offset, [READ_PARAM]),
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
            codes.append(self.program_memory[i])
            if mode == 0:
                # Position Mode (i.e. Reference)
                if arg_type in (READ_PARAM, WRITE_PARAM):
                    inputs.append(self.program_memory[i])
                else:
                    raise ValueError("Invalid parameter type {} for mode {}".format(arg_type, mode))
            elif mode == 1:
                # Intermediate Mode (i.e. Value)
                if arg_type == READ_PARAM:
                    inputs.append(i)
                else:
                    raise ValueError("Invalid parameter type {} for mode {}".format(arg_type, mode))
            elif mode == 2:
                # Relative Mode
                if arg_type in (READ_PARAM, WRITE_PARAM):
                    inputs.append(self.relative_base + self.program_memory[i])
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

    assert IntCodeComputer([1,9,10,3,2,3,11,0,99,30,40,50]).run()[0] == 3500
    assert IntCodeComputer([1,0,0,0,99]).run() == [2,0,0,0,99]
    assert IntCodeComputer([2,3,0,3,99]).run() == [2,3,0,6,99]
    assert IntCodeComputer([2,4,4,5,99, 0]).run() == [2,4,4,5,99,9801]
    assert IntCodeComputer([1,1,1,4,99,5,6,0,99]).run() == [30,1,1,4,2,5,6,0,99]
    output_6 = IntCodeComputer([1, 1, 1, 4, 99, 5, 6, 0, 99]).run(noun=0, verb=1)
    assert output_6 == [11, 0, 1, 4, 1, 5, 6, 0, 99]

    print("Maths Tests Pass")

    test_cases = [
        ([3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], [8], [1]),
        ([3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], [6], [0]),
        ([3,9,7,9,10,9,4,9,99,-1,8], [7], [1]),
        ([3,9,7,9,10,9,4,9,99,-1,8], [9], [0]),
        ([3,3,1108,-1,8,3,4,3,99], [8], [1]),
        ([3,3,1108,-1,8,3,4,3,99], [7], [0]),
        ([3,3,1107,-1,8,3,4,3,99], [7], [1]),
        ([3,3,1107,-1,8,3,4,3,99], [9], [0]),
        ([3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9], [0], [0]),
        ([3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9], [23], [1]),
        ([3,3,1105,-1,9,1101,0,0,12,4,12,99,1], [0], [0]),
        ([3,3,1105,-1,9,1101,0,0,12,4,12,99,1], [32], [1]),
        (
            [
                3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20, 31,
                1106, 0, 36, 98, 0, 0, 1002, 21, 125, 20, 4, 20, 1105, 1, 46, 104,
                999, 1105, 1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1, 46, 98, 99
            ], [7], [999]
        ),
        (
            [
                3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20, 31,
                1106, 0, 36, 98, 0, 0, 1002, 21, 125, 20, 4, 20, 1105, 1, 46, 104,
                999, 1105, 1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1, 46, 98, 99
            ], [8], [1000]
        ),
        (
            [
                3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20, 31,
                1106, 0, 36, 98, 0, 0, 1002, 21, 125, 20, 4, 20, 1105, 1, 46, 104,
                999, 1105, 1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1, 46, 98, 99
            ], [9], [1001]
        ),
    ]
    for program, inputs, expected_outputs in test_cases:
        outputs = []
        computer = IntCodeComputer(program, inputs, outputs)
        computer.run()
        try:
            assert outputs == expected_outputs
        except AssertionError:
            print(program, outputs, expected_outputs)
            raise

    print("Logic and Input Modes 0,1 Tests Pass")

    print("Input Mode 2 Tests Pass")

    print("Tests Done")


if __name__ == "__main__":
    tests()

    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Input")
    program = get_program(input_file)

    computer = IntCodeComputer(program)
    computer.run()
