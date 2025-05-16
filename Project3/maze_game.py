from llstack import *
from typing import Union
from node import *


class InvalidCoordinateError(Exception):
    pass


class OutOfBoundaries(Exception):
    pass


class Map:
    def __init__(self, grid: list[list[str]], start_loc: tuple, end_loc: tuple) -> None:
        """
        Constructor for the Map class.

        :param grid:
            The underlying grid storing the map. The possible values of grid are ocean, grass.
        :param start_loc:
            Tuple representing the start coordinates (row, col).
        :param end_loc:
            Tuple representing the end coordinates (row, col).
        :raises:
            TypeError if the grid is not a list of strings.
        :raises:
            ValueError if the values of the grid are not ocean or grass.
        """

        if not isinstance(grid, list) or not all(isinstance(row, list) for row in grid):
            raise TypeError("Grid must be a list of lists.")

        if not all(isinstance(cell, str) for row in grid for cell in row):
            raise TypeError("All grid values must be strings.")

        if not all(cell in {"ocean", "grass"} for row in grid for cell in row):
            raise ValueError("Grid can only contain 'ocean' or 'grass'.")

        self.__grid = grid
        self.start_coords = start_loc
        self.end_coords = end_loc

    @property
    def start_coords(self) -> tuple:
        """
        Getter method for the start coordinates.

        :return:
            __start (tuple): Tuple representing the start coordinates.
        """
        return self.__start

    @start_coords.setter
    def start_coords(self, value) -> None:
        """
        Setter for the start coordinates.

        :param value:
            Tuple representing the start coordinates (row, col).
        :raises:
            TypeError If the provided value is not a tuple or if the elements of the tuple are not integers.
        :raises:
            ValueError if the tuple does not have exactly two elements, or if any of the elements are negative.
        :raises:
            OutOfBoundaries error if the coordinates specified by the tuple are outside the boundaries of the grid.
        :raises:
            InvalidCoordinateError if the coordinates specified by the tuple point to a cell containing "ocean".
        """

        if not isinstance(value, tuple):
            raise TypeError("Start coordinates must be a tuple.")

        if len(value) != 2:
            raise ValueError("Start coordinates must be a tuple of length 2.")

        if not all(isinstance(i, int) for i in value):
            raise TypeError("Start coordinates must contain integers.")

        if not all(i >= 0 for i in value):
            raise ValueError("Start coordinates must contain positive integers.")

        if not self.__is_within_bounds(value):
            raise OutOfBoundaries("Start coordinates are out of the grid boundaries.")

        if self.__grid[value[0]][value[1]] == "ocean":
            raise InvalidCoordinateError("Start coordinates cannot point to an ocean.")

        self.__start = value

    @property
    def end_coords(self) -> tuple:
        """
        Setter for the end coordinates.

        :return:
            __end (tuple): Tuple representing the end coordinates.
        """
        return self.__end

    @end_coords.setter
    def end_coords(self, value) -> None:
        """
        Setter for the end coordinates.

        :param value:
            Tuple representing the start coordinates (row, col).
        :raises:
            TypeError if the provided value is not a tuple or if the elements of the tuple are not integers.
        :raises:
            ValueError if the tuple does not have exactly two elements, if any of the elements are negative, or if the
            coordinates are the same as the start coordinates.
        :raises:
            OutOfBoundaries error if the coordinates specified by the tuple are outside the boundaries of the grid.
        :raises:
            InvalidCoordinateError if the coordinates specified by the tuple point to a cell containing "ocean".
        """

        if not isinstance(value, tuple):
            raise TypeError("End coordinates must be a tuple.")

        if len(value) != 2:
            raise ValueError("End coordinates must be a tuple of length 2.")

        if not all(isinstance(i, int) for i in value):
            raise TypeError("End coordinates must contain integers.")

        if not all(i >= 0 for i in value):
            raise ValueError("End coordinates must contain positive integers.")

        if not self.__is_within_bounds(value):
            raise OutOfBoundaries("End coordinates are out of the grid boundaries.")

        if self.__grid[value[0]][value[1]] == "ocean":
            raise InvalidCoordinateError("End coordinates cannot point to an ocean.")

        if value == self.__start:
            raise ValueError("End coordinates cannot be the same as start coordinates.")

        self.__end = value

    @property
    def grid(self) -> list[list[str]]:
        """
        Property for the underlying grid storing the map. The possible values of grid are ocean and grass.

        :return:
            __grid(list[list[str]]): A list of lists of strings.
        """

        return self.__grid

    def __is_within_bounds(self, coord) -> list:
        """
        Helper function that checks if a coordinate is within the grid boundaries.

        :param coord:
            Tuple of coordinates (row, col).
        :return:
            True if within bounds, False otherwise.
        """

        row, col = coord
        return 0 <= row < len(self.__grid) and 0 <= col < len(self.__grid[row])

    def find_path(self) -> Union[LLStack, None]:
        """
        The top-level method to solve the maze.

        :return:
            An LLStack representing the valid path through the map, with the exit cell being the node at the top of the
            stack and the entry cell being the node at the bottom. If the map is not solvable, it returns None.
        """

        # Create a stack to store the solution path
        path_stack = LLStack()

        # Set to track visited nodes
        visited = set()

        # Call the recursive solve method and return the path stack if solvable
        if self.solve(self.start_coords, path_stack, visited):
            return path_stack

        # Return None if not solvable
        return None

    def solve(self, current: tuple, path_stack: LLStack, visited: set) -> bool:
        """
        Recursive method to solve the maze.

        :param current:
            The current coordinates (row, col) being traversed through.
        :param path_stack:
            The LLStack representing the current path.
        :param visited:
            A set of visited coordinates to avoid cycles.
        :return:
            True if a solution is found, False otherwise.
        """

        # Base Case 1: If current is the end, add it to the path and return True
        if current == self.end_coords:
            path_stack.push(current)
            return True

        # Base Case 2: If current is invalid or already visited, return False
        if not self.__is_within_bounds(current) or current in visited or self.__grid[current[0]][current[1]] == "ocean":
            return False

        # The current cell is marked as visited
        visited.add(current)

        # Add the current cell to the path stack
        path_stack.push(current)

        # Recursive Case: Explore cells (up, down, left, right)
        row, col = current

        down = (row + 1, col)
        right = (row, col + 1)
        left = (row, col - 1)
        up = (row - 1, col)

        # Explore down
        if self.solve(down, path_stack, visited):
            return True

        # Explore right
        if self.solve(right, path_stack, visited):
            return True

        # Explore left
        if self.solve(left, path_stack, visited):
            return True

        # Explore up
        if self.solve(up, path_stack, visited):
            return True

        # Remove the current cell from the path stack and visited set
        path_stack.pop()
        visited.remove(current)

        # False if no solution is found from this cell
        return False

    def find_shortest_path(self):
        """
        Finds the shortest path through the maze.

        :return:
            An LLStack representing the shortest path through the map, with the exit cell being the node at the top of
            the stack and the entry cell being the node at the bottom. If the map is not solvable, it returns None.
        """

        # Dictionary to store shortest path for each cell
        visited_paths = {}

        # Calls the recursive helper to compute the shortest path
        shortest_path = self.solve_shortest_helper(self.start_coords, visited_paths)

        if not shortest_path:
            return None  # No solution

        # Converts the shortest path to an LLStack
        path_stack = LLStack()
        self.__build_stack(path_stack, shortest_path)
        return path_stack

    def solve_shortest_helper(self, current: tuple, visited_paths: dict) -> Union[list, None]:
        """
        Recursive helper method to compute the shortest path from the current cell to the end.

        :param current:
            The current coordinates (row, col) being traversed.
        :param visited_paths:
            A dictionary to store already-computed the shortest paths for memoization.
        :return:
            A list representing the shortest path from the current cell to the end, or None if no path exists.
        """

        # Base case 1
        if current in visited_paths:
            return visited_paths[current]

        # Base Case 2: If current is invalid or an ocean, return None
        if not self.__is_within_bounds(current) or self.__grid[current[0]][current[1]] == "ocean":
            visited_paths[current] = None
            return None

        # Base Case 3: If current is the end, return a path with just the current cell
        if current == self.end_coords:
            visited_paths[current] = [current]
            return [current]

        visited_paths[current] = None

        # Recursive Case: Explore neighboring cells
        row, col = current

        # Explore right
        path_right = self.solve_shortest_helper((row, col + 1), visited_paths)
        shortest_path = path_right if path_right is not None else None

        # Explore down
        path_down = self.solve_shortest_helper((row + 1, col), visited_paths)
        if path_down is not None and (shortest_path is None or len(path_down) < len(shortest_path)):
            shortest_path = path_down

        # Explore left
        path_left = self.solve_shortest_helper((row, col - 1), visited_paths)
        if path_left is not None and (shortest_path is None or len(path_left) < len(shortest_path)):
            shortest_path = path_left

        # Explore up
        path_up = self.solve_shortest_helper((row - 1, col), visited_paths)
        if path_up is not None and (shortest_path is None or len(path_up) < len(shortest_path)):
            shortest_path = path_up

        # If a valid shortest path is found, append the current cell
        if shortest_path is not None:
            shortest_path = [current] + shortest_path

        # Memorize the result of the current cell
        visited_paths[current] = shortest_path
        return shortest_path

    def __build_stack(self, stack: LLStack, path: list) -> None:
        """
        Helper method to recursively build the LLStack from the shortest path.

        :param stack:
            The LLStack to be built.
        :param path:
            The list of coordinates representing the shortest path.
        """

        if not path:
            return
        stack.push(path[0])
        self.__build_stack(stack, path[1:])


