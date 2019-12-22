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
        self.width = width
        self.height = height
        self.grid = self.generate_grid(width, height)
        self.score = 0
        self.running = False
        self.debug = debug
        self.log_file = log
        self.screen = None
        self.ai = AI(debug=debug, log=log)

    def activate_curses(self):
        self.log_debug("Activating Curses")
        self.screen = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        # self.screen.nodelay(True)
        self.screen.keypad(True)
        self.game_win = curses.newwin(self.height, self.width, 0, 0)
        self.score_win = curses.newwin(10, self.width, self.height, 0)
        self.score_win.addstr(0, 0, "=" * self.width)
        self.score_win.addstr(2, 0, "=" * self.width)

    def deactivate_curses(self):
        self.log_debug("Deactivating Curses")
        curses.nocbreak()
        self.screen.keypad(False)
        curses.echo()
        curses.endwin()

    def log_debug(self, message):
        if self.debug:
            if self.log_file:
                self.log_file.write(message)
                self.log_file.write("\n")
                self.log_file.flush()
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
            if self.screen:
                self.score_win.addstr(1, 0, str(value))
                self.score_win.refresh()
        else:
            # Tile Update
            self.grid[y][x] = value
            if self.screen:
                self.game_win.addstr(y, x, self.tiles[value])
                self.game_win.refresh()

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
            self.game_win.refresh()
            self.score_win.refresh()

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
        elif key == curses.KEY_LEFT:
            # Left arrow ==> (Left Joystick Position)
            self.stdin.put(-1)
        elif key == curses.KEY_RIGHT:
            # Right arrow ==> (Right Joystick Position)
            self.stdin.put(1)
        elif key == -1 or key == curses.KEY_DOWN:
            # No input/Down arrow ==> (Neutral Joystick Position)
            self.stdin.put(0)
        else:
            self.log_debug("Unknown Input: {}".format(key))

    def ai_input(self):
        try:
            move = self.ai.get_next_move(self.grid)
        except Exception as e:
            self.log_debug(str(e))
            move = 0
        self.log_debug("AI Move: {}".format(move))
        self.stdin.put(move)

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
                # time.sleep(0.15)
                # self.read_input()
                self.ai_input()
        except Exception as e:
            self.log_debug(str(e))
        finally:
            self.deactivate_curses()


class AI:

    def __init__(self, debug=True, log=None):
        self.debug = debug
        self.log_file = log

    def log(self, message):
        if self.log_file:
            self.log_file.write(message)
            self.log_file.write("\n")
        else:
            print(message)

    @staticmethod
    def find_ball_location(grid):
        for y, row in enumerate(grid):
            for x, tile_id in enumerate(row):
                if tile_id == 4:
                    return x, y
        raise ValueError("No Ball in Grid!")

    @staticmethod
    def find_paddle_location(grid):
        for y, row in enumerate(grid):
            for x, tile_id in enumerate(row):
                if tile_id == 3:
                    return x, y
        raise ValueError("No Paddle in Grid!")

    def get_next_move(self, grid):
        ball = self.find_ball_location(grid)
        if self.debug:
            self.log("Ball Location: ({},{})".format(*ball))
        paddle = self.find_paddle_location(grid)
        if self.debug:
            self.log("Paddle Location: ({},{})".format(*paddle))

        if ball[0] < paddle[0]:
            # Move Left
            return -1
        elif ball[0] > paddle[0]:
            # Move Right
            return 1
        else:
            # Freeze
            return 0


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
        terminal = Terminal(terminal_socket, joystick_socket, width=38, height=22, debug=True, log=log)
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

    blocks = count_blocks(terminal.grid)
    print(count_blocks(terminal.grid))
    print(terminal.score)

    return blocks


def tests():
    t = Terminal([1,2,3,6,5,4], 10, 10)
    t.run()
    print("Tests Done")


class ArcadeCabinet(IntCodeComputer):

    def __init__(self, program, name="ArcadeCabinet", debug=False, log=None):
        super().__init__(program, name=name, debug=debug, log=log)
        self.terminal = Terminal(width=38, height=22, debug=debug, log=log)
        self.instruction = []
        self.ai = AI(debug=debug, log=log)

    def output(self, address):
        value = self.program_memory[address]
        self.instruction.append(value)
        if len(self.instruction) == 3:
            self.terminal.update(*self.instruction)
            self.terminal.render()
            self.instruction = []

    def input(self, store):
        value = self.ai.get_next_move(self.terminal.grid)
        self.program_memory[store] = value

    def run(self, noun=None, verb=None, memory_allocation_size=None):
        self.terminal.activate_curses()
        try:
            super().run(noun=noun, verb=verb, memory_allocation_size=memory_allocation_size)
        finally:
            self.terminal.deactivate_curses()


if __name__ == "__main__":
    # tests()

    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Input")
    program = get_program(input_file)
    # Insert 2 quarters
    program[0] = 2
    arcade = ArcadeCabinet(program)
    arcade.run(memory_allocation_size=10000)

    print("Blocks:", count_blocks(arcade.terminal.grid))
    print("Score:", arcade.terminal.score)

    if False:
        while True:
            program = get_program(input_file)
            # Insert 2 qurters
            program[0] = 2
            remaining_blocks = run(program)
            if remaining_blocks == 0:
                print("AI WON!")
                break

