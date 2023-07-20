import random
import time
from tkinter import Tk, BOTH, Canvas


def main():
    win = Window(1200, 1000, bg_color="tan", fg_color="black")
    m = Maze(25, 25, 38, 46, 25, 25, win, seed=None)
    m.break_walls()
    solved = m.solve()
    if solved:
        print('Solved!')
    win.wait_for_close()


class Window:
    def __init__(self, width, height, bg_color="black", fg_color="white"):
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.root = Tk()
        self.root.title = "This is a test"
        self.root.wm_title = "Hello"

        self.canvas = Canvas(self.root, bg=self.bg_color,
                             height=height, width=width)

        self.canvas.pack()
        self.running = False
        self.root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.root.update_idletasks()
        self.root.update()

    def wait_for_close(self):
        self.running = True
        while self.running:
            self.redraw()

    def close(self):
        self.running = False

    def draw_line(self, line, fill_color):
        line.draw(self.canvas, fill_color)

    def draw_move(self, to_cell, undo=False):
        color = "red"
        if undo:
            color = "gray"


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, p):
        if self.x != p.x:
            return False
        if self.y != p.y:
            return False
        return True


class Line:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def draw(self, canvas, fill_color):
        x1 = self.p1.x
        x2 = self.p2.x
        y1 = self.p1.y
        y2 = self.p2.y
        canvas.create_line(
            x1, y1, x2, y2, fill=fill_color, width=2
        )
        canvas.pack()

    def __eq__(self, l):
        if self.p1 != l.p1:
            return False
        if self.p2 != l.p2:
            return False
        return True


class Cell:
    def __init__(self, p1, p2, location=None, window=None):
        # location is a tuple, (i, j), where the cell
        # exists in the maze.
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self._x1 = 0
        self._x2 = 0
        self._y1 = 0
        self._y2 = 0
        self._win = window
        self.visited = False
        self.end_cell = False
        self.location = location

        if p1.x < p2.x:
            self._x1, self._x2 = p1.x, p2.x
        else:
            self._x1, self._x2 = p2.x, p1.x
        if p1.y < p2.y:
            self._y1, self._y2 = p1.y, p2.y
        else:
            self._y1, self._y2 = p2.y, p1.y

    def draw(self):
        if not self._win:
            return
        tl_point = Point(self._x1, self._y1)
        tr_point = Point(self._x2, self._y1)
        bl_point = Point(self._x1, self._y2)
        br_point = Point(self._x2, self._y2)
        lw = Line(tl_point, bl_point)
        rw = Line(tr_point, br_point)
        tw = Line(tl_point, tr_point)
        bw = Line(bl_point, br_point)
        if self.has_left_wall:
            lw.draw(self._win.canvas, self._win.fg_color)
        else:
            lw.draw(self._win.canvas, self._win.bg_color)
        if self.has_right_wall:
            rw.draw(self._win.canvas, self._win.fg_color)
        else:
            rw.draw(self._win.canvas, self._win.bg_color)
        if self.has_top_wall:
            tw.draw(self._win.canvas, self._win.fg_color)
        else:
            tw.draw(self._win.canvas, self._win.bg_color)
        if self.has_bottom_wall:
            bw.draw(self._win.canvas, self._win.fg_color)
        else:
            bw.draw(self._win.canvas, self._win.bg_color)

    def get_center(self):
        x = (self._x1 + self._x2) // 2
        y = (self._y1 + self._y2) // 2
        return Point(x, y)

    def draw_move(self, to_cell, undo=False):
        color = "red"
        if undo:
            color = "gray"

        line = Line(self.get_center(), to_cell.get_center())
        line.draw(self._win.canvas, color)

    def __repr__(self):
        return f"Cell(Point({self._x1}, {self._y1}), Point({self._x2}, {self._y2}))"

    def __eq__(self, c):
        if self._x1 != c._x1:
            return False
        if self._x2 != c._x2:
            return False
        if self._y1 != c._y1:
            return False
        if self._y2 != c._y2:
            return False
        if self.has_left_wall != c.has_left_wall:
            return False
        if self.has_right_wall != c.has_right_wall:
            return False
        if self.has_top_wall != c.has_top_wall:
            return False
        if self.has_bottom_wall != c.has_bottom_wall:
            return False
        return True


class Maze:
    def __init__(self, x1, y1, num_rows, num_cols,
                 cell_size_x, cell_size_y, win=None, seed=None):
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        if seed is not None:
            random.seed(seed)

        self._create_cells()

    def _get_x_or_y_vals(self, start_pos, cell_size, number):
        xy1 = start_pos + (cell_size * number)
        xy2 = xy1 + cell_size
        return xy1, xy2

    def _create_cells(self):
        self._cells = []
        for i in range(self._num_rows):
            y1, y2 = self._get_x_or_y_vals(self._y1, self._cell_size_y, i)
            row = []
            for j in range(self._num_cols):
                x1, x2 = self._get_x_or_y_vals(self._x1, self._cell_size_x, j)
                p1 = Point(x1, y1)
                p2 = Point(x2, y2)
                row.append(Cell(p1, p2, (i, j), self._win))
            self._cells.append(row)

        for row in self._cells:
            for cell in row:
                cell.draw()

    def _animate(self):
        self._win.redraw()
        time.sleep(0.05)

    def _break_entrance_and_exit(self):
        tl = self._cells[0][0]
        br = self._cells[self._num_rows - 1][self._num_cols - 1]
        br.end_cell = True
        tl.has_top_wall = False
        tl.draw()
        br.has_bottom_wall = False
        br.draw()

    def _get_neighbor_cell(self, current, direction):
        # current is current cell object, direction is one
        # of r, l, u, d
        i_diff = 0
        j_diff = 0
        if direction == 'r':
            j_diff = 1
        elif direction == 'l':
            j_diff = -1
        elif direction == 'u':
            i_diff = -1
        elif direction == 'd':
            i_diff = 1

        new_i = current.location[0] + i_diff
        new_j = current.location[1] + j_diff
        if new_i < 0 or new_j < 0:
            return None

        try:
            new_cell = self._cells[new_i][new_j]
        except IndexError:
            return None

        return new_cell

    def _break_walls_between_cells(self, current, new, direction):
        if direction == 'r':
            current.has_right_wall = False
            new.has_left_wall = False
            return
        if direction == 'l':
            current.has_left_wall = False
            new.has_right_wall = False
            return
        if direction == 'u':
            current.has_top_wall = False
            new.has_bottom_wall = False
            return
        if direction == 'd':
            current.has_bottom_wall = False
            new.has_top_wall = False
            return
        return

    def break_walls(self):
        self._reset_cells_visited()
        self._break_entrance_and_exit()
        start_cell = self._cells[0][0]
        self._break_walls_r(start_cell)

    def _break_walls_r(self, current):
        current.visited = True
        while True:
            to_visit = []
            for direction in ['r', 'l', 'u', 'd']:
                new_cell = self._get_neighbor_cell(current, direction)
                if new_cell is None:
                    continue
                if not new_cell.visited:
                    to_visit.append((new_cell, direction))
            if not to_visit:
                current.draw()
                return
            new_cell, direction = random.choice(to_visit)
            self._break_walls_between_cells(current, new_cell, direction)
            self._break_walls_r(new_cell)

    def _reset_cells_visited(self):
        for row in self._cells:
            for cell in row:
                cell.visited = False

    def solve(self):
        self._reset_cells_visited()
        start_cell = self._cells[0][0]
        return self._solve_r(start_cell)

    def _solve_r(self, current):
        self._animate()
        current.visited = True
        if current.end_cell:
            return True
        directions = []
        if not current.has_left_wall:
            directions.append('l')
        if not current.has_right_wall:
            directions.append('r')
        if not current.has_top_wall:
            directions.append('u')
        if not current.has_bottom_wall:
            directions.append('d')

        for direction in directions:
            ncell = self._get_neighbor_cell(current, direction)
            if ncell and not ncell.visited:
                current.draw_move(ncell)
                solved = self._solve_r(ncell)
                if solved:
                    return True
                else:
                    current.draw_move(ncell, undo=True)
        return False


if __name__ == "__main__":
    main()
