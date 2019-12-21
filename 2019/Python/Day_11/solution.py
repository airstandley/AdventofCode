import os
import threading
import queue

from utils.grid_tools_2d import Point, Vector
from utils.intcode_computer import IntCodeComputer, get_program


def get_input(filepath):
    # Load the comma separated intcode program from a file into memory (a list).
    with open(filepath) as f:
        data = [line.strip() for line in f]
    return


BLACK = 0
WHITE = 1


class PaintRobot:
    debug = False
    READ_TIMEOUT = 10
    WRITE_TIMEOUT = 10

    def __init__(self, program, grid, starting_position, starting_facing):
        """
        :param List[int] -> program:
        :param List[List[int]] -> grid:
        :param Point -> starting_position:
        :param Vector -> starting_facing:
        """
        self.grid = grid
        self.position = starting_position
        self.direction = starting_facing
        self.optical_scanner = queue.Queue(1)
        self.move_instructions = queue.Queue(2)
        self.brain = IntCodeComputer(
            program, input_queue=self.optical_scanner, output_queue=self.move_instructions, name="PainterBrain"
        )
        self.brain.debug = self.debug
        self.running = False
        # Track panels visited for the Part 1
        self.visited_panels = {self.position}

    def scan_panel(self):
        color = self.grid[self.position.y][self.position.x]
        if color == BLACK:
            # Send 0
            self.optical_scanner.put(0, timeout=self.WRITE_TIMEOUT)
            if self.debug:
                print("Painter scanner put BLACK", self.optical_scanner.qsize())
        elif color == WHITE:
            # Send 1
            self.optical_scanner.put(1, timeout=self.WRITE_TIMEOUT)
            if self.debug:
                print("Painter scanner put WHITE", self.optical_scanner.qsize())
        else:
            raise RuntimeError("Unknown Panel Color '{}'".format(color))

    def get_next_instruction(self):
        if self.debug:
            print("Getting instructions from brain...")
        color = self.move_instructions.get(timeout=self.READ_TIMEOUT)
        if self.debug:
            print("Painter got color code", color)
        direction = self.move_instructions.get(timeout=self.READ_TIMEOUT)
        if self.debug:
            print("Painter got direction code", direction)
        return color, direction

    def set_direction(self, direction_code):
        if direction_code == 0:
            # Turn left 90 degrees
            self.direction.rotate(-90)
            self.direction = self.direction.nearest_integer()
            if self.debug:
                print("Turned left 90. New direction: {}".format(self.direction))
        elif direction_code == 1:
            # Turn right 90 degrees
            self.direction.rotate(90)
            self.direction = self.direction.nearest_integer()
            if self.debug:
                print("Turned right 90. New direction: {}".format(self.direction))
        else:
            raise RuntimeError("Unknown Direction Code '{}'".format(direction_code))

    def paint_panel(self, color_code):
        if color_code == 0:
            # Paint it black
            self.grid[self.position.y][self.position.x] = BLACK
            if self.debug:
                print("Painted Panel at {} BLACK".format(self.position))
        elif color_code == 1:
            # Paint it white
            self.grid[self.position.y][self.position.x] = WHITE
            if self.debug:
                print("Painted Panel at {} WHITE".format(self.position))
        else:
            raise RuntimeError("Unknown Paint Code '{}'".format(color_code))

    def move(self):
        self.position += self.direction
        if self.debug:
            print("Moved to Panel at {}".format(self.position))
        self.visited_panels.add(self.position)

    def stop(self):
        self.running = False

    def run(self):
        brain_thread = threading.Thread(target=lambda: self.brain.run(memory_allocation_size=10000))
        brain_thread.start()
        self.running = True
        while self.running:
            if self.debug:
                print('Tick')
            if not self.brain.running:
                self.stop()
                continue
            try:
                self.scan_panel()
                color, direction = self.get_next_instruction()
                self.paint_panel(color)
                self.set_direction(direction)
                self.move()
            except BaseException as e:
                print("Exception:", e)
                self.stop()
        # Terminate the brain
        if brain_thread.is_alive():
            self.brain.running = False
            brain_thread.join()

        print(len(self.visited_panels))


def tests():
    pass
    print("Tests Done")


if __name__ == "__main__":
    tests()

    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Input")
    program = get_program(input_file)

    panel_grid = [
        list([BLACK]) * 80 for _ in range(30)
    ]

    starting_position = Point(10, 10)
    panel_grid[starting_position.y][starting_position.x] = WHITE

    painter = PaintRobot(program, panel_grid, starting_position, Vector(0, -1))
    painter.run()

    for row in panel_grid:
        output = ""
        for panel in row:
            if panel == BLACK:
                output += "*"
            elif panel == WHITE:
                output += " "
        print(output)