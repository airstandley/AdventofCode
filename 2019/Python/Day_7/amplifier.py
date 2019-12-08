import os
import copy
import threading
import queue
from itertools import permutations
from intcode_computer import get_program, IntCodeComputer


class AmplifierIntCodeComputer(IntCodeComputer):
    """
    IntCode computer that takes inputs and writes outputs via queues. Designed to run in it's own thread.
    """

    def __init__(self, program, input_queue, output_queue):
        self.program = copy.copy(program)
        self.input_queue = input_queue
        self.output_queue = output_queue

    def run(self):
        return super().run(copy.copy(self.program))

    def input(self, store_pos):
        input_value = self.input_queue.get()
        self.program[store_pos] = input_value

    def output(self, value):
        self.output_queue.put(value)


class AmplifierCircuit:

    def __init__(self, program):
        self.io_queues = [
            queue.Queue(2),
            queue.Queue(2),
            queue.Queue(2),
            queue.Queue(2),
            queue.Queue(2),
        ]
        self.circuit = [
            AmplifierIntCodeComputer(program, self.io_queues[0], self.io_queues[1]),
            AmplifierIntCodeComputer(program, self.io_queues[1], self.io_queues[2]),
            AmplifierIntCodeComputer(program, self.io_queues[2], self.io_queues[3]),
            AmplifierIntCodeComputer(program, self.io_queues[3], self.io_queues[4]),
            AmplifierIntCodeComputer(program, self.io_queues[4], self.io_queues[0])
        ]

    def run(self, phase_settings):
        for io_queue, phase_setting in zip(self.io_queues, phase_settings):
            io_queue.put_nowait(phase_setting)
        self.io_queues[0].put_nowait(0)

        # Start the amplifiers
        threads = []
        for amplifier in self.circuit:
            thread = threading.Thread(target=amplifier.run)
            threads.append(thread)
            thread.start()

        # Block until all threads are done
        for thread in threads:
            thread.join()

        output = self.io_queues[0].get_nowait()
        return output


def calculate_max_phase_setting(circuit):
    max_thrust = 0
    max_phase_settings = None
    for phase_settings in permutations(range(5)):
        thrust = circuit.run(phase_settings)
        if thrust > max_thrust:
            max_thrust = thrust
            max_phase_settings = phase_settings
    return max_phase_settings, max_thrust


def tests():
    program_1 = [3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]
    circuit_1 = AmplifierCircuit(program_1)
    phase_sequence_1 = (4,3,2,1,0)
    max_thrust_1 = 43210

    program_2 = [3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0]
    circuit_2 = AmplifierCircuit(program_2)
    phase_sequence_2 = (0,1,2,3,4)
    max_thrust_2 = 54321

    program_3 = [3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0]
    circuit_3 = AmplifierCircuit(program_3)
    phase_sequence_3 = (1,0,4,3,2)
    max_thrust_3 = 65210

    # Check thrust computation is correct
    assert circuit_1.run(phase_sequence_1) == max_thrust_1
    assert circuit_2.run(phase_sequence_2) == max_thrust_2
    assert circuit_3.run(phase_sequence_3) == max_thrust_3

    # Check brute force maximum calculation
    assert calculate_max_phase_setting(circuit_1)[0] == phase_sequence_1
    assert calculate_max_phase_setting(circuit_2)[0] == phase_sequence_2
    assert calculate_max_phase_setting(circuit_3)[0] == phase_sequence_3


if __name__ == "__main__":
    tests()
    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Input")
    program = get_program(input_file)
    circuit = AmplifierCircuit(program)
    print(calculate_max_phase_setting(circuit))
