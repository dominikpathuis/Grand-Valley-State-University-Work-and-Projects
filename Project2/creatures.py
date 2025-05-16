from __future__ import annotations
from random import randint
from typing import Optional, Union, List
from coord import Coord
from character import Character, Player
from abc import ABC, abstractmethod


class Villain(Character):
    def __init__(self) -> None:
        """
        Constructor for the Villain class, setting the player as a Villain.
        """
        super().__init__(Player.VILLAIN)

    def is_valid_move(self, from_coord: Coord, to_coord: Coord, board: List[List[Union[None, Character]]]) -> bool:
        """
        Checks for valid Villain movement, ensuring movement is restricted to one direction horizontally or vertically
        and within the Villain's maximum movement range. Villains cannot move diagonally or switch directions.

        :param from_coord:
            The starting coordinates.
        :param to_coord:
            The ending coordinates.
        :param board:
            The 2-dimensional list representing the game board.
        :return:
            (bool): True if the movement is valid for a Villain, False otherwise.
        """
        if not super().is_valid_move(from_coord, to_coord, board):
            return False

        horizontal_move = abs(to_coord.x - from_coord.x)
        vertical_move = abs(to_coord.y - from_coord.y)

        # Checks for either horizontal or vertical movement, not both
        if horizontal_move > 0 and vertical_move > 0:
            return False

        if horizontal_move > self.move or vertical_move > self.move:
            return False

        if horizontal_move > 0:
            if to_coord.x > from_coord.x:
                step = 1
            else:
                step = -1

            for i in range(from_coord.x + step, to_coord.x, step):
                if board[i][from_coord.y] is not None:
                    return False

        if vertical_move > 0:
            if to_coord.y > from_coord.y:
                step = 1
            else:
                step = -1

            for i in range(from_coord.y + step, to_coord.y, step):
                if board[from_coord.x][i] is not None:
                    return False

        return True

    def is_valid_attack(self, from_coord: Coord, to_coord: Coord, board: List[List[Union[None, Character]]]) -> bool:
        """
        Inherits the method from the Character class and checks if the starting and ending coordinates are in bounds
        and are different, the starting location is the self, and the ending location is not None.

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
        return super().is_valid_attack(from_coord, to_coord, board)

    def calculate_dice(self, attack=True, lst: list = [], *args, **kwargs) -> int:
        """
        Inherits the method from the Character class and implements the rules for calculating dice, where the attacking
        player rolls as many dice as their attack attribute and counts how many die are greater than 4, the defending
        player rolls as many dice as their defense attribute and counts how many die are greater than 3, and lastly,
        subtracting the defense total from the attack total. If the result is greater than 0, the defending character
        receives that amount of damage.

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
        return super().calculate_dice(attack, lst, *args, **kwargs)

    def deal_damage(self, target: Character, damage: int, *args, **kwargs) -> None:
        """
        Inherits the method from the Character class and selects a target character and deducts damage from their
        __temp_health.

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
        return super().deal_damage(target, damage, *args, **kwargs)


class Goblin(Villain):
    def __init__(self) -> None:
        """
        Constructor for the Goblin class that sets custom stats for a Goblin.
        """
        super().__init__()
        self.health = 3
        self.temp_health = 3
        self.combat = [2, 2]


class Skeleton(Villain):
    def __init__(self) -> None:
        """
        Constructor for the Skeleton class that sets custom stats for a Skeleton.
        """
        super().__init__()
        self.health = 2
        self.temp_health = 2
        self.combat = [2, 1]
        self.move = 2


class Necromancer(Villain):
    def __init__(self) -> None:
        """
        Constructor for the Necromancer class that sets custom stats for a Necromancer.
        """
        super().__init__()
        self.combat = [1, 2]
        self.range = 3

    def raise_dead(self, target: Character, from_coords: Coord, to_coords: Coord,
                   board: List[List[Union[None, Character]]]) -> None:
        """
        Allows the Necromancer to raise a dead target that is within range, converting it to a Villain if not one
        already and setting its temp_health to half its health, regardless of the player type (Hero or Villain).

        :param target:
            The Character target that is selected in range to be raised.
        :param from_coords:
            The starting coordinates.
        :param to_coords:
            The ending coordinates.
        :param board:
            A 2-dimensional list that is the playing board.
        """

        horizontal_move = abs(from_coords.x - to_coords.x)
        vertical_move = abs(from_coords.y - to_coords.y)

        if horizontal_move > self.range or vertical_move > self.range:
            print("The target is out of range!")
            return None

        if target.temp_health > 0:
            print(f'{target} cannot be raised. It is still alive!')
            return None

        if target.player != Player.VILLAIN:
            target.player = Player.VILLAIN
            print(f'{target} has been transformed into a Villain!')

        target.temp_health = target.health // 2


class Hero(Character):
    def __init__(self) -> None:
        """
        Constructor for the Hero class, setting the player as a Hero.
        """
        super().__init__(Player.HERO)

    def is_valid_move(self, from_coord: Coord, to_coord: Coord, board: List[List[Union[None, Character]]]) -> bool:
        """
        Verifies if movement is valid for a Hero Character, following the base method's requirements.

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
        return super().is_valid_move(from_coord, to_coord, board)

    def is_valid_attack(self, from_coord: Coord, to_coord: Coord, board: List[List[Union[None, Character]]]) -> bool:
        """
        Verifies if attack is valid for a Hero character, following the base method's requirements.

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
        return super().is_valid_attack(from_coord, to_coord, board)

    def calculate_dice(self, attack=True, lst: list = [], *args, **kwargs) -> int:
        """
        Implements dice calculation rules for Heroes, following the base method's requirements.

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
        return super().calculate_dice(attack, lst, *args, **kwargs)

    def deal_damage(self, target: Character, damage: int, *args, **kwargs) -> None:
        """
        Selects a target character and deducts damage from their __temp_health by following the base method's
        requirements.

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
        return super().deal_damage(target, damage, *args, **kwargs)


class Warrior(Hero):
    def __init__(self) -> None:
        """
        Constructor for the Warrior class that sets custom stats for a Warrior.
        """
        super().__init__()
        self.health = 7
        self.temp_health = 7
        self.combat = [2, 4]

    def calculate_dice(self, target: Character, attack=True, lst: list = [], gob: list = []) -> int:
        """
        Calculates the outcome of dice rolls based on the Warrior's stats and adds two additional dice if attacking a
        Goblin.

        :param target:
            The Character type.
        :param attack:
            Signifies that the self is attacking the target.
        :param lst:
            Holds a series of integers between 1-6 in place of randomly generating those numbers based on the __attack
            or __defense
        :param gob:
            A list that holds two values 1-6.
        :return:
            (int): Returns the sum of successful rolls.
        """

        super().calculate_dice(target=target, attack=attack, lst=lst)

        if attack:
            num_dice = self.combat[0]
        else:
            num_dice = self.combat[1]

        dice_rolls = lst[:num_dice]
        dice_rolls.extend([randint(1, 6)])

        if attack:
            success_criteria = 5
        else:
            success_criteria = 4

        if attack and isinstance(target, Goblin):
            self.combat[0] += 2
            if not gob:
                dice_rolls.extend([randint(1, 6), randint(1, 6)])

        successful_rolls = 0
        for roll in dice_rolls:
            if roll >= success_criteria:
                successful_rolls += 1

        return successful_rolls


class Mage(Hero):
    def __init__(self) -> None:
        """
        Constructor for the Mage class that sets custom stats for a Mage.
        """
        super().__init__()
        self.combat = [2, 2]
        self.range = 3
        self.move = 2

    def deal_damage(self, target: Character, damage: int) -> None:
        """
        A method that selects a target character and deducts damage from their __temp_health.
        :param target:
            Character that the damage is being dealt to.
        :param damage:
            The amount of damage being dealt to the target.
        """
        target.temp_health -= damage + 1


class Paladin(Hero):
    def __init__(self) -> None:
        """
        Constructor for the Paladin class that sets custom stats for a Paladin.
        """
        super().__init__()
        self.__heal = True
        self.health = 6
        self.temp_health = 6

    @property
    def heal(self) -> bool:
        """
        Property for the heal attribute.

        :return:
            __heal (bool): Denotes whether the heal ability has been used on the current board or not.
        """
        return self.__heal

    @heal.setter
    def heal(self, value) -> None:
        """
        Setter for the heal attribute.

        :param value:
            the __heal value to be set.
        :raises:
            TypeError exception if __heal is not True or False (bool).
        """
        if isinstance(value, bool):
            self.__heal = value
        else:
            raise TypeError('Heal must be a boolean value: True or False')

    def revive(self, target: Character, from_coord: Coord, to_coord: Coord,
               board: List[List[Union[None, Character]]]) -> None:
        """
        Resets the target's temp_health to half of the value of base health rounded down if they are in range. This
        method only works if heal is True. Using this method sets heal to False.

        :param target:
            The Character target that will be revived.
        :param from_coord:
            The starting coordinates.
        :param to_coord:
            The ending coordinates.
        :param board:
            A 2-dimensional list that is the playing board.
        """

        horizontal_move = abs(from_coord.x - to_coord.x)
        vertical_move = abs(from_coord.y - to_coord.y)

        if horizontal_move > self.range or vertical_move > self.range:
            print("The target is out of range!")
            return None

        if not self.__heal:
            print("Heal ability has already been used!")
            return None

        if target.temp_health == 0:
            target.temp_health = target.health // 2
            print(f'{target} has been revived!')

            self.__heal = False

        else:
            print(f'{target} cannot be revived. They are not dead!')


class Ranger(Hero):
    def __init__(self) -> None:
        """
        Constructor for the Ranger class that sets custom stats for a Ranger.
        """
        super().__init__()
        self.range = 3

    def deal_damage(self, target: Character, damage: int) -> None:
        """
        Selects a target character and deducts damage from their __temp_health. If the target is a Skeleton, the Ranger
        deals 1 less damage that normal.

        :param target:
            Character that the damage is being dealt to.
        :param damage:
            The amount of damage being dealt
        """
        if isinstance(target, Skeleton):
            target.temp_health -= damage - 1
        else:
            target.temp_health -= damage

        if damage < 0:
            target.temp_health = 0
