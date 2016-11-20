"""Abstractions related to the game and game logic"""


class Cell:
    """Represents one element of the board"""
    def __init__(self, z=0, active=False, lit=False):  # setting default values
        self.z = z
        self.active = active
        self.lit = lit

    def __repr__(self):
        return 'z = {}, active = {}, lit up = {}'.format(self.z, self.active, self.lit)


class Board:
    """Represents the board"""
    def __init__(self, filename: str):
        """Reads a board file from disk and stores it as a Board object."""
        with open(filename) as f:
            header = f.readline().strip()

            # Making massive tuple unpacking here
            (self.width, self.height, self.start_x,
             self.start_y, self.angle) = map(int, header.split())

            # Making an empty board (i.e. list of lists)
            temp_list = [Cell() for _ in range(self.width)]
            self.cells = [temp_list for _ in range(self.height)]
            for x, line in enumerate(f.read().splitlines()):
                for y, curr_cell in enumerate(map(int, line.split())):
                    self.cells[x][y] = Cell(abs(curr_cell), curr_cell < 0)

    def draw(self) -> None:
        """Prettyprinting a board."""
        for x in range(self.width):
            for y in range(self.height):
                print(self.cells[x][y])
            print()


if __name__ == '__main__':
    board = Board('board.txt')
    board.draw()
