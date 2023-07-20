import unittest

from maze import Line, Maze, Point, Cell


class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m1._cells),
            num_rows,
        )
        self.assertEqual(
            len(m1._cells[0]),
            num_cols,
        )

    def test_break_entrance_exit(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        m1._break_entrance_and_exit()
        tl = m1._cells[0][0]
        br = m1._cells[num_rows - 1][num_cols - 1]
        self.assertFalse(tl.has_top_wall)
        self.assertTrue(tl.has_bottom_wall)
        self.assertFalse(br.has_bottom_wall)
        self.assertTrue(br.has_top_wall)

    def test_cell_location(self):
        num_cols = 10
        num_rows = 20
        cell_size_x = 50
        cell_size_y = 20
        start_x = 10
        start_y = 20
        # Define bottom right cell in maze
        # vertical lines should be at 460 and 510 (x values)
        # horizontal lines should be at 400 and 420 (y values)
        p1 = Point(460, 400)
        p2 = Point(510, 420)
        expected_cell = Cell(p1, p2)

        m1 = Maze(start_x, start_y, num_rows,
                  num_cols, cell_size_x, cell_size_y)
        self.assertEqual(m1._cells[num_rows - 1][num_cols - 1], expected_cell)

    def test_cell_normalize(self):
        tl = Point(100, 101)
        tr = Point(200, 101)
        bl = Point(100, 201)
        br = Point(200, 201)

        c1 = Cell(tl, br)
        c2 = Cell(tr, bl)

        self.assertEqual(c1, c2)

    def test_cell_get_center(self):
        p1 = Point(100, 200)
        p2 = Point(300, 400)
        exp_center = Point(200, 300)
        c1 = Cell(p1, p2)
        center = c1.get_center()
        self.assertEqual(center, exp_center)

    def test_line_equal(self):
        l1 = Line(Point(100, 200), Point(300, 400))
        l2 = Line(Point(100, 200), Point(300, 400))
        self.assertEqual(l1, l2)

    def test_reset_visited(self):
        m = Maze(0, 0, 10, 10, 10, 10)
        self.assertFalse(m._cells[1][3].visited)
        self.assertFalse(m._cells[4][8].visited)
        self.assertFalse(m._cells[9][4].visited)
        m._cells[1][3].visited = True
        m._cells[4][8].visited = True
        m._cells[9][4].visited = True
        self.assertTrue(m._cells[1][3].visited)
        self.assertTrue(m._cells[4][8].visited)
        self.assertTrue(m._cells[9][4].visited)
        m._reset_cells_visited()
        self.assertFalse(m._cells[1][3].visited)
        self.assertFalse(m._cells[4][8].visited)
        self.assertFalse(m._cells[9][4].visited)


if __name__ == "__main__":
    unittest.main()
