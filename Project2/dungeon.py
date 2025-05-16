from random import randint
from typing import List, Optional, Union
from creatures import Goblin, Skeleton, Necromancer, Hero, Villain, Warrior, Mage, Paladin, Ranger
from character import Player
from coord import Coord


class Dungeon:
    def __init__(self, height: int, width: int, villains: List[Villain] = []) -> None:
        """
        Constructor for the Dungeon class that creates the game board and initializes the game characters.

        :param height:
            Determines the number of rows on the dungeon __board.
        :param width:
            Determines the number of columns on the dungeon __board.
        :param villains:
            Holds the Villain pieces of the current __board
        """
        if not isinstance(height, int):
            raise TypeError

        if not isinstance(width, int):
            raise TypeError

        if not isinstance(villains, list):
            raise TypeError

        if not (4 <= height <= 12):
            raise ValueError

        if not (4 <= width <= 12):
            raise ValueError

        self.__height = height
        self.__width = width
        self.__board = [[None for _ in range(self.__width)] for _ in range(self.__height)]
        self.__player = Player.HERO
        self.__heroes = [Warrior(), Mage(), Paladin(), Ranger()]
        if len(villains) == 0:
            self.generate_villains()
        else:
            for i in villains:
                if not isinstance(i, Villain):
                    raise TypeError
            self.__villains = villains

    @property
    def height(self) -> int:
        """
        Property for the height attribute.

        :return:
            __height (int): The height of the generated board.
        """
        return self.__height

    @property
    def width(self) -> int:
        """
        Property for the width attribute.

        :return:
            __width (int): The width of the generated board.
        """
        return self.__width

    @property
    def board(self) -> list:
        """
        Property for the board attribute.

        :return:
        __board (int): A 2-dimensional list where each cell can contain a Character or None.
        """
        return self.__board

    @board.setter
    def board(self, value) -> None:
        """
        Setter for the board attribute.

        :param value:
            The __board value to be set.
        :raises:
            TypeError exception if __board is not a list.
        """
        if isinstance(value, list):
            self.__board = [[None for _ in range(self.__width)] for _ in range(self.__height)]
        else:
            raise TypeError

    @property
    def player(self) -> Player:
        """
        Property for the player attribute.

        :return:
        __player (enum): The currently playing team.
        """
        return self.__player

    @property
    def heroes(self) -> list:
        """
        Property for the heroes attribute.

        :return:
            __heroes (list): The list of current Heroes on the board.
        """
        return self.__heroes

    @heroes.setter
    def heroes(self, value) -> None:
        """
        Setter for the heroes attribute.

        :param value:
            The __heroes value to be set.
        :raises:
            TypeError exception if __heroes is not a list.
        """
        if isinstance(value, list):
            for i in value:
                if i.player == Player.HERO:
                    pass
                else:
                    raise TypeError
            self.__heroes = value
        else:
            raise TypeError

    @property
    def villains(self) -> list:
        """
        Property for the villains attribute.

        :return:
            __villains (list): The list of current Villains on the board.
        """
        return self.__villains

    @villains.setter
    def villains(self, value) -> None:
        """
        Setter for the villains attribute.

        :param value:
            The __villains value being set.
        :raises:
            TypeError exception if __villains is not a list.
        """
        if isinstance(value, list):
            for i in value:
                if i.player == Player.VILLAIN:
                    pass
                else:
                    raise TypeError
            self.__villains = value
        else:
            raise TypeError

    def generate_villains(self) -> None:
        """
        Generates a list of villains for the board. Goblins have a 50% chance of spawning, Skeletons have a 30% chance
        of spawning, and Necromancers have a 20% chance of spawning. If a Necromancer has already spawned, the next
        Necromancer will instead be a Skeleton.
        """
        villain_count = randint(1, max(self.__height, self.__width))
        villains = []
        necromancer_added = False

        for _ in range(villain_count):
            villain_type = randint(1, 10)
            if villain_type <= 5:
                villains.append(Goblin())
            elif villain_type <= 8:
                villains.append(Skeleton())
            elif villain_type >= 9 and not necromancer_added:
                villains.append(Necromancer())
                necromancer_added = True
            else:
                villains.append(Skeleton())

        self.__villains = villains

    def is_valid_move(self, coords: List[Coord]) -> bool:
        """
        Checks whether a character can move from a place on the board to another based on the input coords.

        :param coords:
            The coordinate pair where the character that wants to move is at, and where the character wants to go.
        :return:
            (bool): Returns a bool of whether the coordinates produce a valid move or not.
        """
        if len(coords) < 2:
            return False
        if len(coords) > 2 and self.player == Player.HERO:
            return True
        if len(coords) > 2 and self.player == Player.VILLAIN:
            return False

        for coord in coords:
            if not (0 <= coord.x < self.__height) or not (0 <= coord.y < self.__width):
                return False
        return True

    def is_valid_attack(self, coords: List[Coord]) -> bool:
        """
        Checks whether a character can attack another character of the opposite team based on if the input coords
        produce a valid attack.

        :param coords:
            The coordinate pair where the character that wants to move is at, and where the character wants to attack.
        :return:
            (bool): Returns a bool of whether the coordinates produce a valid attack.
        """
        if len(coords) < 2:
            return False
        if len(coords) > 2 and self.player == Player.HERO:
            return True
        if len(coords) > 2 and self.player == Player.VILLAIN:
            return False

        for coord in coords:
            if not (0 <= coord.x < self.__height) or not (0 <= coord.y < self.__width):
                return False
        return True

    def character_at(self, x: int, y: int) -> Optional[Union[Hero, Villain]]:
        """
        Returns a Character at a given spot on the board.
        :param x:
            The height value on the board to be checked.
        :param y:
            The width value on the board to be checked.
        :return:
            The value of a certain cell on the board, which is either of type Character or None.
        :raises:
            ValueError exception if coordinates are out of bounds.
        """
        if not (0 <= x < self.__height and 0 <= y < self.__width):
            raise ValueError("Coordinates are out of bounds")
        return self.__board[x][y]

    def set_character_at(self, target: Union[Hero, Villain], x: int, y: int) -> None:
        """
        Sets the selected character to a given x and y position on the board.

        :param target:
            The character to be set to a new position.
        :param x:
            The height value on the board to be checked.
        :param y:
            The width value on the board to be checked.
        :raises:
            ValueError exception if coordinates are out of bounds.
        """
        if not (0 <= x < self.__height and 0 <= y < self.__width):
            raise ValueError("Coordinates are out of bounds")
        self.__board[x][y] = target

    def move(self, from_coord: Coord, to_coord: Coord) -> None:
        """
        Moves the value stored at from_coord and places it at to_coord.

        :param from_coord:
            The coordinates of the character to be moved.
        :param to_coord:
            The coordinates that the character is moved to.
        """
        character = self.character_at(from_coord.x, from_coord.y)
        if character and self.is_valid_move([from_coord, to_coord]):
            self.set_character_at(character, to_coord.x, to_coord.y)
            self.set_character_at(None, from_coord.x, from_coord.y)

    def attack(self, from_coords: Coord, to_coords: Coord) -> None:
        """
        Checks to see the from_coords and to_coords produce a valid attack. If so, it calculates and deals damage to the
        Character at the location of the to_coords.

        :param from_coords:
            The coordinates of the character attacking.
        :param to_coords:
            The coordinates of the character defending.
        """
        current = self.board[from_coords.x][from_coords.y]
        attack_validity = current.is_valid_attack(from_coords, to_coords, self.board)

        if attack_validity:
            attacker = self.board[from_coords.x][from_coords.y]
            defender = self.board[to_coords.x][to_coords.y]

            if str(attacker) == str('Warrior'):
                damage = attacker.calculate_dice(defender, attack_validity, [1, 6], [1, 6])
            else:
                damage = attacker.calculate_dice(attack_validity, [1, 6])

            if damage == 0:
                print(f"{defender} took no damage from {attacker}")

            else:
                attacker.deal_damage(defender, damage)

    def set_next_player(self) -> None:
        """
        Toggles back and forth between the __player attribute between HERO and VILLAIN.
        """
        if self.__player == Player.HERO:
            self.__player = Player.VILLAIN
        else:
            self.__player = Player.HERO

    def is_dungeon_clear(self) -> bool:
        """
        Checks if every Villain's health has fallen to zero, indicating that the dungeon has been cleared.

        :return:
            (bool): True if every Villain's health is at zero. False otherwise.
        """
        count = 0

        for row in self.board:
            for cell in row:
                if isinstance(cell, Villain) and cell.temp_health > 0:
                    return False
                if isinstance(cell, Hero) and cell.temp_health > 0:
                    count += 1
        if count > 0:
            return True
        else:
            return False

    def adventurer_defeat(self) -> bool:
        """
        Checks if every Heroes health has fallen to zero, indicating that the Heroes have been defeated.

        :return:
            (bool): True if every Heroes health is at zero. False otherwise.
        """
        for row in self.board:
            for cell in row:
                if isinstance(cell, Hero) and cell.temp_health > 0:
                    return False
        return True

    def place_heroes(self) -> None:
        """
        This method places the heroes on the bottom two rows in the middle. On an even board, the Warrior will be placed
         to the left of the middle on the second to last row and the Paladin to its right. Behind them are the Mage and
         Ranger respectively. If the board is odd, place the Warrior directly on the middle index.
        """
        middle = self.__width // 2
        if self.__width % 2 == 0:
            self.set_character_at(self.__heroes[0], self.__height - 2, middle - 1)
            self.set_character_at(self.__heroes[2], self.__height - 2, middle)
            self.set_character_at(self.__heroes[1], self.__height - 1, middle - 1)
            self.set_character_at(self.__heroes[3], self.__height - 1, middle)
        else:
            self.set_character_at(self.__heroes[0], self.__height - 2, middle)
            self.set_character_at(self.__heroes[2], self.__height - 2, middle + 1)
            self.set_character_at(self.__heroes[1], self.__height - 1, middle - 1)
            self.set_character_at(self.__heroes[3], self.__height - 1, middle + 1)

    def place_villains(self) -> None:
        """
        Randomly places all the villains on the board except on the bottom two rows.
        """
        for villain in self.__villains:
            while True:
                x = randint(0, self.__height - 3)
                y = randint(0, self.__width - 1)
                if self.character_at(x, y) is None:
                    self.set_character_at(villain, x, y)
                    break

    def generate_new_board(self, height: int = -1, width: int = -1) -> None:
        """
        Creates a new board based on a new height and width. If no arguments are given height and width will be random
        numbers between 4 and 12. This will generate new villains and place both heroes and villains on the board.

        :param height:
            The height for the new board.
        :param width:
            The width for the new board.
        """
        self.__height = randint(4, 12) if height == -1 else height
        self.__width = randint(4, 12) if width == -1 else width
        self.__board = [[None for _ in range(self.__width)] for _ in range(self.__height)]
        self.generate_villains()
        self.place_heroes()
        self.place_villains()

    def print_board(self) -> None:
        """
        Prints the current state of the __board.
        """
        st = ' \t'
        st += '_____' * len(self.board)
        st += '\n'
        for i in range(len(self.__board)):
            st += f'{i}\t'
            for j in range(len(self.__board[i])):
                if self.board[i][j] is None:
                    st += '|___|'
                else:
                    st += f'|{self.board[i][j].__class__.__name__[:3]}|'
            st += '\n'
        st += '\t'
        for i in range(len(self.board[0])):
            st += f'  {i}  '
        print(st)
