import os
import copy

def get_program(filepath):
    # Load the comma separated intcode program from a file into memory (a list).
    with open(filepath) as f:
        incode = [int(v) for v in f.readline().split(",")]
    return incode


class IntCodeComputer:

    @staticmethod
    def restore_state(program, noun, verb):
        program[1] = noun
        program[2] = verb
        return program

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


def noun_verb_search(program, desired_output):
    computer = IntCodeComputer()
    for noun in range(100):
        for verb in range(100):
            test_state = copy.copy(program)
            computer.restore_state(test_state, noun, verb)
            output = computer.run(test_state)[0]
            if output == desired_output:
                return noun, verb
    raise ValueError("Desired value {} is unreachable!".format(desired_output))


if __name__ == "__main__":
    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Input")
    program = get_program(input_file)

    noun, verb = noun_verb_search(program, 19690720)
    print("Solution:", 100 * noun + verb, "Noun:", noun, "Verb:", verb)


def tests():
    computer = IntCodeComputer()

    assert computer.run([1,9,10,3,2,3,11,0,99,30,40,50])[0] == 3500
    assert computer.run([1,0,0,0,99,0,0,0]) == [2,0,0,0,99,0,0,0]
    assert computer.run([2,3,0,3,99,0,0,0]) == [2,3,0,6,99,0,0,0]
    assert computer.run([2,4,4,5,99,0,0,0]) == [2,4,4,5,99,9801,0,0]
    assert computer.run([1,1,1,4,99,5,6,0,99,0,0,0]) == [30,1,1,4,2,5,6,0,99,0,0,0]