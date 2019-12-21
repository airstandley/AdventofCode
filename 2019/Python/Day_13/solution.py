import os
import threading
import queue
import time

from utils.grid_tools_2d import Point, Vector
from utils.intcode_computer import IntCodeComputer, get_program

import curses

debug_log = "debug.txt"


class Terminal:
    tiles = {
        0: " ",
        1: "█",
        2: "▒",
        3: "=",
        4: "*",
    }

    def __init__(self, stdout=None, stdin=None, width=10, height=10, debug=False, log=None):
        self.stdout = stdout
        self.stdin = stdin
        self.grid = self.generate_grid(width, height)
        self.score = 0
        self.running = False
        self.debug = debug
        self.debug_log = log
        self.screen = None

    def activate_curses(self):
        self.log_debug("Activating Curses")
        self.screen = curses.initscr()
        curses.noecho()
        curses.cbreak()
        # self.screen.nodelay(True)
        self.screen.keypad(True)

    def deactivate_curses(self):
        self.log_debug("Deactivating Curses")
        curses.nocbreak()
        self.screen.keypad(False)
        curses.echo()
        curses.endwin()

    def log_debug(self, message):
        if self.debug:
            if self.debug_log:
                self.debug_log.write(message)
                self.debug_log.write("\n")
                self.debug_log.flush()
            else:
                print(message)

    @staticmethod
    def generate_grid(width, height):
        grid = []
        for _ in range(height):
            grid.append([0]*width)
        return grid

    def update(self, x, y, value):
        self.log_debug("Update: ({}, {}) {}".format(x, y, value))
        if x == -1 and y == 0:
            # Score Update
            self.score = value
        else:
            # Tile Update
            self.grid[y][x] = value
            if self.screen:
                self.screen.addstr(y, x, self.tiles[value])

    def vanilla_render(self):
        if not self.debug:
            print(chr(27) + "[2J")
        print("====================")
        for row in self.grid:
            line = ""
            for tile_id in row:
                line += self.tiles[tile_id]
            print(line)
        print("====================")
        print(self.score)
        print("====================")

    def render(self):
        if self.screen is None:
            self.vanilla_render()
        else:
            self.screen.refresh()

    def read_stdout(self):
        if self.stdout is None:
            value = int(input("Input:"))
        elif hasattr(self.stdout, 'get'):
            value = self.stdout.get()
            # timeouts = 0
            # while self.running and timeouts < self.MAX_TIMEOUTS:
            #     try:
            #         value = self.input_queue.get(timeout=self.READ_TIMEOUT)
            #     except queue.Empty:
            #         timeouts += 1
            #         if self.debug:
            #             print("Input Timeout {} ({})".format(timeouts, self.input_queue.qsize()))
        elif hasattr(self.stdout, 'pop'):
            value = self.stdout.pop(0)
        else:
            raise RuntimeError("Invalid input configured.")

        return value

    def read_input(self):
        key = self.screen.getch()
        if key == ord('q'):
            # Quit
            self.running = False
            return 0
        elif key == curses.KEY_LEFT:
            # Left arrow (Left Joystick Position)
            return -1
        elif key == curses.KEY_RIGHT:
            # Right arrow (Right Joystick Position)
            return 1
        elif key == -1:
            # No input (Neutral Joystick Position)
            return 0
        else:
            self.log_debug("Unknown Input: {}".format(key))
            return 0

    def process_events(self):
        if self.stdout.qsize() >= 3:
            x = self.read_stdout()
            y = self.read_stdout()
            tile_id = self.read_stdout()
            self.update(x, y, tile_id)
            return True
        return False

    def run(self):
        self.running = True
        self.activate_curses()
        try:
            while self.running:
                self.render()
                if self.process_events():
                    continue  # Keep processing
                time.sleep(1)
                self.stdin.put(self.read_input())
        except Exception as e:
            self.log_debug(str(e))
        finally:
            self.deactivate_curses()


def count_blocks(grid):
    blocks = 0
    for row in grid:
        for tile_id in row:
            if tile_id == 2:
                blocks += 1
    return blocks


def run(program):
    terminal_socket = queue.Queue()
    joystick_socket = queue.Queue()
    with open(debug_log, mode="w") as log:
        terminal = Terminal(terminal_socket, joystick_socket, 50, 50, debug=True, log=log)
        computer = IntCodeComputer(
            program, input_queue=joystick_socket, output_queue=terminal_socket, name="ArcadeCabinet",
            debug=True, log=log
        )
        computation_thread = threading.Thread(target=lambda: computer.run(memory_allocation_size=10000))
        gui_thread = threading.Thread(target=lambda: terminal.run())

        try:
            computation_thread.start()
            gui_thread.start()
        except:
            computer.running = False
            terminal.running = False

        computation_thread.join()
        while terminal_socket.qsize() > 0:
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
    # Insert 2 qurters
    program[0] = 2

    run(program)
