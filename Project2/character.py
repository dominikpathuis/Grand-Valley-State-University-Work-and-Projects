from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional, Union, List
from enum import Enum
from random import randint
from coord import Coord


class CharacterDeath(Exception):

    def __init__(self, msg, char: Character) -> None:
        """
        Constructor for the CharacterDeath class, which is a custom exception.

        :param msg:
            The message displayed if exception is raised.
        :param char:
            The Character class information that will be passed if exception is raised.
        """
        self.message = msg
        char.temp_health = 0


class InvalidAttack(Exception):
    """
    Custom exception that can be raised for an invalid attack.
    """
    pass


class Player(Enum):
    """
    Sets VILLAIN and HERO as Enums.
    """
    VILLAIN = 0
    HERO = 1


class Character(ABC):

    @abstractmethod
    def __init__(self, player: Player) -> None:
        """
        Constructor for the Character class that sets all starting statistics.

        :param
            player: The player team of the character, an Enum provided in the Player class (VILLAIN or HERO).
        """
        self.__player = player
        self.__health = 5
        self.__temp_health = 5
        self.__attack = 3
        self.__defense = 3
        self.__move = 3
        self.__range = 1

    @property
    def player(self) -> Player:
        """
        Property for the player attribute.

        :return:
            __player (Enum): The currently playing team.
        """
        return self.__player

    @player.setter
    def player(self, value) -> None:
        """
        Setter for the player attribute.

        :param value:
            The new player to be set.
        :raises:
            TypeError exception if value os not a Player Enum.
        """
        if not isinstance(value, Player):
            raise TypeError("Player must be of type Player enum")
        else:
            self.__player = value

    @property
    def health(self) -> int:
        """
        Property for the health attribute.

        :return:
            __health (int): The maximum amount of health points a Character can have.
        """
        return self.__health

    @health.setter
    def health(self, value) -> None:
        """
        Setter for the health attribute.

        :param value:
            The new health amount to be set.
        :raises:
            ValueError exception if health is less than 0.

        """
        if value >= 0:
            self.__health = value
        else:
            raise ValueError('Health must be 0 or more.')

    @property
    def temp_health(self) -> int:
        """
        Property for temp_health attribute.

        :return:
            __temp_health (int): The current amount of health points a Character has.
        """
        return self.__temp_health

    @temp_health.setter
    def temp_health(self, value) -> None:
        """
        Setter for the temp_health attribute.

        :param value:
            The new temp_health amount to be set.
        :raises:
            CharacterDeath exception if the Character has been killed.
        """
        if value < 0:
            raise CharacterDeath('Character has been Unalived', self)
        else:
            self.__temp_health = value

    @property
    def combat(self) -> list:
        """
        Property for combat attribute.

        :return:
            __attack (int): The amount of dice the Character rolls when attempting to deal damage.
            __defense (int): The amount of dice the Character rolls when attempting to prevent damage.
            Both are returned as a list with attack in element 0, and defense in element 1.
        """
        return [self.__attack, self.__defense]

    @combat.setter
    def combat(self, values) -> None:
        """
        Setter for combat attribute.

        :param values:
            The new __attack and __defense values to be set.
        :raises:
            TypeError exception if values is not a list.
            ValueError exception if values does not contain a list with length 2, with both elements being > 0.
        """
        if not isinstance(values, list):
            raise TypeError('Combat must be a list of two non-negative integers [attack, defense]')

        if not len(values) == 2 or not values[0] >= 0 or not values[1] >= 0:
            raise ValueError('Combat must be a list of two non-negative integers [attack, defense]')

        else:
            self.__attack, self.__defense = values[0], values[1]

    @property
    def range(self) -> int:
        """
        Property for the range attribute.

        :return:
            __range (int): The amount of spaces away a Character can hit another Character.
        """
        return self.__range

    @range.setter
    def range(self, value) -> None:
        """
        Setter for the range attribute.

        :param value:
            The new __range value to be set.
        :raises:
            ValueError exception if the range is less than 1.
        """
        if value > 0:
            self.__range = value
        else:
            raise ValueError('Range must be at least 1')

    @property
    def move(self) -> int:
        """
        Property for the move attribute.

        :return:
            __move (int): The amount of spaces a Character can move on the board.
        """
        return self.__move

    @move.setter
    def move(self, value) -> None:
        """
        Setter for the move attribute.

        :param value:
            The __move value to be set.
        :raises:
            ValueError if move is less than 1.
        """
        if value > 0:
            self.__move = value
        else:
            raise ValueError('Move must be greater than 0')

    @abstractmethod
    def is_valid_move(self, from_coord: Coord, to_coord: Coord, board: List[List[Union[None, Character]]]) -> bool:
        """
        Abstract method that checks if the starting and ending coordinates are in bounds and are different, the self
        Character is at the starting location, and that the ending location is empty.

        :param from_coord:
            The starting coordinates.
        :param to_coord:
            The ending coordinates.
        :param board:
            A 2-dimensional list that is the playing board.

        :return:
            (bool): True if the start coordinates point to a valid character that is on the correct team, and the end
            coordinates point to an end location that is not occupied. False otherwise.
        """

        # Check that the starting coordinates are in bounds
        if not (0 <= from_coord.x < len(board)) or not (0 <= from_coord.y < len(board[0])):
            return False

        # Check that the ending coordinates are in bounds
        if not (0 <= to_coord.x < len(board)) or not (0 <= to_coord.y < len(board[0])):
            return False

        # Ensure the starting and ending coordinates are different
        if board[from_coord.x][from_coord.y] == board[to_coord.x][to_coord.y]:
            return False

        # Ensure that self Character is at the starting location
        if board[from_coord.x][from_coord.y] is not self:
            return False

        # Ensure that the ending location is empty
        if board[to_coord.x][to_coord.y] is not None:
            return False

        # Otherwise, return True
        return True

    @abstractmethod
    def is_valid_attack(self, from_coord: Coord, to_coord: Coord, board: List[List[Union[None, Character]]]) -> bool:
        """
        Abstract method that checks if the starting and ending coordinates are in bounds and are different, the starting
        location is the self, and the ending location is not None.

        :param from_coord:
            The starting coordinates.
        :param to_coord:
            The ending coordinates.
        :param board:
            A 2-dimensional list that is the playing board.
        :return:
            (bool): True if the start coordinates point to a valid character that is on the correct team, and the end
            coordinates point to an end location that is  occupied with the apposing team. False otherwise.
        """

        if not (0 <= from_coord.x < len(board)) or not (0 <= from_coord.y < len(board[0])):
            return False

        if not (0 <= to_coord.x < len(board)) or not (0 <= to_coord.y < len(board[0])):
            return False

        if board[from_coord.x][from_coord.y] == board[to_coord.x][to_coord.y]:
            return False

        if board[from_coord.x][from_coord.y] is not self:
            return False

        if board[to_coord.x][to_coord.y] is None:
            return False

        return True

    @abstractmethod
    def calculate_dice(self, attack=True, lst: list = [], *args, **kwargs) -> int:
        """
        Abstract method that implements the rules for calculating dice, where the attacking player rolls as many dice as
        their attack attribute and counts how many die are greater than 4, the defending player rolls as many dice as
        their defense attribute and counts how many die are greater than 3, and lastly, subtracting the defense total
        from the attack total. If the result is greater than 0, the defending character receives that amount of damage.

        :param attack:
            Signifies that the self is attacking the target.
        :param lst:
            Holds a series of integers between 1-6 in place of randomly generating those numbers based on the __attack
            or __defense.
        :param args:
            Used to pass a variable number of non-keyword arguments.
        :param kwargs:
            Used to pass a variable number of keyword arguments.
        :return:
            (int): Returns the sum of successful rolls.
        """

        if attack:
            num_dice = self.__attack
        else:
            num_dice = self.__defense

        dice_rolls = lst[:num_dice]
        dice_rolls.extend([randint(1, 6)])

        if attack:
            success_criteria = 5
        else:
            success_criteria = 4

        successful_rolls = 0

        for roll in dice_rolls:
            if roll >= success_criteria:
                successful_rolls += 1

        return successful_rolls

    @abstractmethod
    def deal_damage(self, target: Character, damage: int, *args, **kwargs) -> None:
        """
        Abstract method that selects a target character and deducts damage from their __temp_health.

        :param target:
            Character that the damage is being dealt to.
        :param damage:
            The amount of damage being dealt.
        :param args:
            Used to pass a variable number of non-keyword arguments.
        :param kwargs:
            Used to pass a variable number of keyword arguments.
        :raises:
            CharacterDeath exception if the __temp_health is 0.
        """
        try:
            target.temp_health -= damage
            print(f'{str(target)} was dealt {damage} damage!')

        except CharacterDeath as death:
            print(death.message)

    def __str__(self) -> str:
        """
        Built-in python method to return a desired string.

        :return:
            (str): Returns the class name.
        """
        return self.__class__.__name__
