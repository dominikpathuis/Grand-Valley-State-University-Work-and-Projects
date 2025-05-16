import unittest
from llstack import *
from maze_game import *


class LLStackTest(unittest.TestCase):
    def setUp(self):
        self.stack = LLStack()

    def test_push_valid_data(self):

        self.stack.push((0, 0))
        self.assertEqual(self.stack.size, 1)
        self.assertEqual(str(self.stack), "(0,0)")

        self.stack.push((1, 1))
        self.assertEqual(self.stack.size, 2)
        self.assertEqual(str(self.stack), "(0,0) -> (1,1)")

    def test_push_invalid_data(self):
        with self.assertRaises(TypeError):
            self.stack.push([1, 1])

        with self.assertRaises(ValueError):
            self.stack.push((1, -1))

        with self.assertRaises(ValueError):
            self.stack.push((1,))

    def test_pop(self):
        self.stack.push((0, 0))
        self.stack.push((1, 1))

        top = self.stack.pop()
        self.assertEqual(top, (1, 1))
        self.assertEqual(self.stack.size, 1)
        self.assertEqual(str(self.stack), "(0,0)")

        top = self.stack.pop()
        self.assertEqual(top, (0, 0))
        self.assertEqual(self.stack.size, 0)

        with self.assertRaises(IndexError):
            self.stack.pop()

    def test_str_non_empty_stack(self):
        self.stack.push((0, 0))
        self.stack.push((1, 1))
        self.stack.push((2, 2))
        self.assertEqual(str(self.stack), "(0,0) -> (1,1) -> (2,2)")

    def test_size_property(self):
        self.assertEqual(self.stack.size, 0)

        self.stack.push((0, 0))
        self.assertEqual(self.stack.size, 1)

        self.stack.push((1, 1))
        self.assertEqual(self.stack.size, 2)

        self.stack.pop()
        self.assertEqual(self.stack.size, 1)

        self.stack.pop()
        self.assertEqual(self.stack.size, 0)

    def test_stack_integrity_after_exceptions(self):
        self.stack.push((1, 1))
        self.assertEqual(self.stack.size, 1)
        with self.assertRaises(ValueError):
            self.stack.push((1, -1))
        self.assertEqual(self.stack.size, 1)
        self.assertEqual(str(self.stack), "(1,1)")


class GameTest(unittest.TestCase):
    def setUp(self):
        self.grid = [
            ["grass", "ocean", "grass", "grass"],
            ["grass", "grass", "grass", "grass"],
            ["ocean", "grass", "grass", "ocean"],
            ["grass", "grass", "grass", "grass"]
        ]
        self.start_coords = (1, 1)
        self.end_coords = (3, 3)

        self.map = Map(self.grid, self.start_coords, self.end_coords)

    def test_valid_constructor(self):
        self.assertEqual(self.map.start_coords, self.start_coords)
        self.assertEqual(self.map.end_coords, self.end_coords)
        self.assertEqual(self.map.grid, self.grid)

    def test_invalid_grid_type(self):
        with self.assertRaises(TypeError):
            Map("invalid_grid", self.start_coords, self.end_coords)

    def test_invalid_grid_values(self):
        invalid_grid = [
            ["grass", "grass", "invalid"],
            ["ocean", "ocean", "grass"]
        ]
        with self.assertRaises(ValueError):
            Map(invalid_grid, self.start_coords, self.end_coords)

    def test_start_coords_invalid_type(self):
        with self.assertRaises(TypeError):
            self.map.start_coords = "invalid"

    def test_start_coords_invalid_value(self):
        with self.assertRaises(ValueError):
            self.map.start_coords = (-1, 2)

        with self.assertRaises(OutOfBoundaries):
            self.map.start_coords = (4, 4)

        with self.assertRaises(InvalidCoordinateError):
            self.map.start_coords = (2, 0)

    def test_end_coords_invalid_type(self):
        with self.assertRaises(TypeError):
            self.map.end_coords = "invalid"

    def test_end_coords_invalid_value(self):
        with self.assertRaises(ValueError):
            self.map.end_coords = (1, -1)

        with self.assertRaises(OutOfBoundaries):
            self.map.end_coords = (4, 4)

        with self.assertRaises(InvalidCoordinateError):
            self.map.end_coords = (0, 1)

        with self.assertRaises(ValueError):
            self.map.end_coords = self.start_coords

    def test_find_path_valid(self):
        path = self.map.find_path()
        self.assertIsInstance(path, LLStack)
        self.assertNotEqual(path.size, 0)

    def test_find_path_no_path(self):
        grid = [
            ["grass", "ocean", "ocean"],
            ["ocean", "grass", "ocean"],
            ["ocean", "ocean", "grass"]
        ]
        map_obj = Map(grid, (0, 0), (2, 2))
        path = map_obj.find_path()
        self.assertIsNone(path)

    def test_find_shortest_path_valid(self):
        path = self.map.find_shortest_path()
        self.assertIsInstance(path, LLStack)
        self.assertNotEqual(path.size, 0)

    def test_find_shortest_path_no_path(self):
        grid = [
            ["grass", "ocean", "ocean"],
            ["ocean", "grass", "ocean"],
            ["ocean", "ocean", "grass"]
        ]
        map_obj = Map(grid, (0, 0), (2, 2))
        path = map_obj.find_shortest_path()
        self.assertIsNone(path)

    def test_shortest_path_with_dead_end(self):
        grid = [
            ["grass", "grass", "ocean"],
            ["grass", "ocean", "grass"],
            ["grass", "grass", "grass"]
        ]
        map_obj = Map(grid, (0, 0), (2, 2))
        path = map_obj.find_shortest_path()
        self.assertIsInstance(path, LLStack)
        self.assertEqual(str(path), "(0,0) -> (1,0) -> (2,0) -> (2,1) -> (2,2)")

    def test_shortest_path_complex_maze(self):
        grid = [
            ["grass", "grass", "ocean", "grass"],
            ["grass", "ocean", "grass", "grass"],
            ["grass", "grass", "grass", "ocean"],
            ["ocean", "grass", "grass", "grass"]
        ]
        map_obj = Map(grid, (0, 0), (3, 3))
        path = map_obj.find_shortest_path()
        self.assertIsInstance(path, LLStack)
        self.assertEqual(str(path), "(0,0) -> (1,0) -> (2,0) -> (2,1) -> (2,2) -> (3,2) -> (3,3)")

        with self.assertRaises(OutOfBoundaries):
            Map(self.grid, (0, 0), (4, 3))

    def test_invalid_path_grid_values(self):
        invalid_grid = [
            ["grass", "ocean", "invalid"],
            ["ocean", "grass", "grass"]
        ]
        with self.assertRaises(ValueError):
            Map(invalid_grid, (0, 0), (1, 2))

    def test_start_and_end_on_edges(self):
        grid = [
            ["grass", "ocean", "grass", "grass"],
            ["grass", "grass", "grass", "ocean"],
            ["ocean", "grass", "grass", "grass"]
        ]
        map_obj = Map(grid, (0, 0), (2, 3))
        path = map_obj.find_shortest_path()
        self.assertEqual(str(path), "(0,0) -> (1,0) -> (1,1) -> (1,2) -> (2,2) -> (2,3)")

    def test_invalid_start_and_end_assignment(self):
        with self.assertRaises(ValueError):
            self.map.start_coords = (-1, -1)
        with self.assertRaises(InvalidCoordinateError):
            self.map.end_coords = (0, 1)

    def test_rectangular_grid(self):
        grid = [
            ["grass", "grass", "grass", "ocean", "grass"],
            ["grass", "ocean", "grass", "grass", "grass"],
            ["ocean", "grass", "grass", "grass", "grass"]
        ]
        map_obj = Map(grid, (0, 0), (2, 4))
        path = map_obj.find_shortest_path()
        self.assertIsNotNone(path)


if __name__ == '__main__':
    unittest.main()
