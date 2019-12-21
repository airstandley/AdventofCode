import os
import threading
import queue

from utils.grid_tools_2d import Point, Vector
from utils.intcode_computer import IntCodeComputer, get_program


class Terminal:
    tiles = {
        0: " ",
        1: "W",
        2: "B",
        3: "P",
        4: "B",
    }

    def __init__(self, input_queue=None, width=10, height=10, debug=True):
        self.input_queue = input_queue
        self.grid = self.generate_grid(width, height)
        self.running = False
        self.debug = debug

    @staticmethod
    def generate_grid(width, height):
        grid = []
        for _ in range(height):
            grid.append([0]*width)
        return grid

    def update(self, x, y, tile_id):
        if self.debug:
            print("Update:", "({}, {})".format(x, y), "{}:{}".format(tile_id, self.tiles[tile_id]))
        self.grid[y][x] = tile_id

    def render(self):
        if not self.debug:
            print(chr(27) + "[2J")
        print("====================")
        for row in self.grid:
            line = ""
            for tile_id in row:
                line += self.tiles[tile_id]
            print(line)
        print("====================")

    def input(self):
        if self.input_queue is None:
            value = int(input("Input:"))
        elif hasattr(self.input_queue, 'get'):
            value = self.input_queue.get()
            # timeouts = 0
            # while self.running and timeouts < self.MAX_TIMEOUTS:
            #     try:
            #         value = self.input_queue.get(timeout=self.READ_TIMEOUT)
            #     except queue.Empty:
            #         timeouts += 1
            #         if self.debug:
            #             print("Input Timeout {} ({})".format(timeouts, self.input_queue.qsize()))
        elif hasattr(self.input_queue, 'pop'):
            value = self.input_queue.pop(0)
        else:
            raise RuntimeError("Invalid input configured.")

        return value

    def run(self):
        self.running = True
        while self.running:
            try:
                x = self.input()
                y = self.input()
                tile_id = self.input()
                self.update(x, y, tile_id)
                self.render()
            except IndexError as e:
                if self.debug:
                    print(e)
                break


def count_blocks(grid):
    blocks = 0
    for row in grid:
        for tile_id in row:
            if tile_id == 2:
                blocks += 1
    return blocks


def run(program):
    socket = queue.Queue()
    computer = IntCodeComputer(
        program, output_queue=socket, name="ArcadeCabinet"
    )
    # computer.debug = True
    terminal = Terminal(socket, 50, 50)
    computation_thread = threading.Thread(target=lambda: computer.run(memory_allocation_size=10000))
    gui_thread = threading.Thread(target=lambda: terminal.run())

    computation_thread.start()
    gui_thread.start()
    computation_thread.join()
    while socket.qsize() > 0:
        pass
    terminal.running = False
    gui_thread.join()

    print(count_blocks(terminal.grid))


def tests():
    t = Terminal([1,2,3,6,5,4], 10, 10)
    t.run()
    print("Tests Done")


if __name__ == "__main__":
    # tests()

    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Input")
    program = get_program(input_file)

    run(program)
