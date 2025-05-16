import unittest
from character import Character, Player, CharacterDeath, InvalidAttack
from creatures import Goblin, Skeleton, Necromancer, Hero, Warrior, Mage, Paladin, Ranger, Villain
from dungeon import Dungeon
from coord import Coord


# Testing Character-related functionality
class TestCharacter(unittest.TestCase):

    def test_character_player(self):
        self.assertTrue(hasattr(Character, 'player'))
        self.assertIsInstance(getattr(Character, 'player'), property)

    def test_player_setter(self):
        player = Character.player
        with self.assertRaises(TypeError):
            player(1)  # Must be Player enum
        with self.assertRaises(TypeError):
            player('string')  # Must be Player enum
        with self.assertRaises(TypeError):
            player([])  # Must be Player enum
        with self.assertRaises(TypeError):
            player({})  # Must be Player enum

    def test_health_setter(self):
        hero = Warrior()
        hero.health = 10
        self.assertEqual(hero.health, 10)
        with self.assertRaises(ValueError):
            hero.health = -1

    def test_temp_health_setter(self):
        hero = Warrior()
        with self.assertRaises(CharacterDeath):
            hero.temp_health = -1  # Should trigger CharacterDeath

    def test_combat_setter(self):
        hero = Warrior()
        hero.combat = [4, 5]
        self.assertEqual(hero.combat, [4, 5])
        with self.assertRaises(ValueError):
            hero.combat = [4]  # Invalid length
        with self.assertRaises(TypeError):
            hero.combat = 'Can\'t be a string'
        with self.assertRaises(TypeError):
            hero.combat = {}  # Can't be a dict

    def test_range_setter(self):
        hero = Warrior()
        hero.range = 1
        self.assertEqual(hero.range, 1)
        with self.assertRaises(ValueError):
            hero.range = 0

    def test_move_setter(self):
        hero = Warrior()
        hero.move = 3
        self.assertEqual(hero.move, 3)
        with self.assertRaises(ValueError):
            hero.move = 0

    def test_is_valid_move(self):
        board = [[None for _ in range(5)] for _ in range(5)]
        hero = Warrior()
        board[0][0] = hero
        from_coord = Coord(0, 0)
        to_coord = Coord(1, 0)
        self.assertTrue(hero.is_valid_move(from_coord, to_coord, board))

    def test_is_valid_attack(self):
        board = [[None for _ in range(5)] for _ in range(5)]
        hero = Warrior()
        villain = Skeleton()
        board[0][0] = hero
        board[1][0] = villain
        self.assertTrue(hero.is_valid_attack(Coord(0, 0), Coord(1, 0), board))

    def test_calculate_dice(self):
        hero = Warrior()
        target = Goblin()  # Could be any other character instance as the target
        self.assertIn(hero.calculate_dice(target, attack=True, lst=[5, 6]), range(0, 7))

    def test_deal_damage(self):
        hero = Warrior()
        target = Goblin()
        hero.deal_damage(target, 2)
        self.assertEqual(target.temp_health, target.health - 2)

    def test_deal_excessive_damage(self):
        hero = Warrior()
        target = Goblin()
        initial_health = target.temp_health
        hero.deal_damage(target, initial_health + 5)  # Deal more damage than health
        self.assertEqual(target.temp_health, 0)


# Testing Creature-Related functionality
class TestCreatures(unittest.TestCase):

    def setUp(self):
        self.board = [[None] * 10 for _ in range(10)]
        self.goblin = Goblin()
        self.skeleton = Skeleton()
        self.necromancer = Necromancer()
        self.paladin = Paladin()
        self.warrior = Warrior()
        self.ranger = Ranger()
        self.mage = Mage()

    def test_villain_move_validity(self):
        villain = Goblin()
        board = [[None for _ in range(5)] for _ in range(5)]
        board[0][0] = villain
        from_coord = Coord(0, 0)
        to_coord = Coord(2, 0)
        self.assertTrue(villain.is_valid_move(from_coord, to_coord, board))

    def test_goblin(self):
        goblin = Goblin()
        self.assertEqual(len(goblin.combat), 2)
        with self.assertRaises(ValueError):
            goblin.combat = [5]  # Must be length of 2
        self.assertIsInstance(goblin.health, int)
        self.assertIsInstance(goblin.temp_health, int)
        self.assertIsInstance(goblin.combat, list)
        self.assertIsInstance(goblin.move, int)
        self.assertIsInstance(goblin.range, int)

        goblin.combat = [2, 2]
        goblin.health = 3
        goblin.temp_health = 3
        goblin.move = 2
        goblin.range = 1
        self.assertEqual(goblin.combat, [2, 2])
        self.assertEqual(goblin.health, 3)
        self.assertEqual(goblin.temp_health, 3)
        self.assertEqual(goblin.move, 2)
        self.assertEqual(goblin.range, 1)

    def test_goblin_move(self):
        goblin = Goblin()
        from_coord = Coord(2, 2)
        to_coord = Coord(2, 4)  # Too far for a Goblin
        self.assertFalse(goblin.is_valid_move(from_coord, to_coord, self.board))

        to_coord = Coord(3, 2)  # Within range
        self.assertFalse(goblin.is_valid_move(from_coord, to_coord, self.board))

    def test_skeleton(self):
        skeleton = Skeleton()
        self.assertEqual(len(skeleton.combat), 2)
        with self.assertRaises(ValueError):
            skeleton.combat = [5]  # Must be length of 2
        self.assertIsInstance(skeleton.health, int)
        self.assertIsInstance(skeleton.temp_health, int)
        self.assertIsInstance(skeleton.combat, list)
        self.assertIsInstance(skeleton.move, int)
        self.assertIsInstance(skeleton.range, int)

        skeleton.combat = [2, 1]
        skeleton.health = 2
        skeleton.temp_health = 2
        skeleton.move = 2
        skeleton.range = 1
        self.assertEqual(skeleton.combat, [2, 1])
        self.assertEqual(skeleton.health, 2)
        self.assertEqual(skeleton.temp_health, 2)
        self.assertEqual(skeleton.move, 2)
        self.assertEqual(skeleton.range, 1)

    def test_necromancer(self):
        necro = Necromancer()
        self.assertEqual(len(necro.combat), 2)
        with self.assertRaises(ValueError):
            necro.combat = [5]  # Must be length of 2
        self.assertIsInstance(necro.health, int)
        self.assertIsInstance(necro.temp_health, int)
        self.assertIsInstance(necro.combat, list)
        self.assertIsInstance(necro.move, int)
        self.assertIsInstance(necro.range, int)

        necro.combat = [2, 1]
        necro.health = 2
        necro.temp_health = 2
        necro.move = 3
        necro.range = 3
        self.assertEqual(necro.combat, [2, 1])
        self.assertEqual(necro.health, 2)
        self.assertEqual(necro.temp_health, 2)
        self.assertEqual(necro.move, 3)
        self.assertEqual(necro.range, 3)

    def test_warrior(self):
        warrior = Warrior()
        self.assertEqual(len(warrior.combat), 2)
        with self.assertRaises(ValueError):
            warrior.combat = [5]  # Must be length of 2
        self.assertIsInstance(warrior.health, int)
        self.assertIsInstance(warrior.temp_health, int)
        self.assertIsInstance(warrior.combat, list)
        self.assertIsInstance(warrior.move, int)
        self.assertIsInstance(warrior.range, int)

        warrior.combat = [2, 4]
        warrior.health = 7
        warrior.temp_health = 7
        warrior.move = 3
        warrior.range = 1
        self.assertEqual(warrior.combat, [2, 4])
        self.assertEqual(warrior.health, 7)
        self.assertEqual(warrior.temp_health, 7)
        self.assertEqual(warrior.move, 3)
        self.assertEqual(warrior.range, 1)

    def test_mage(self):
        mage = Mage()
        self.assertEqual(len(mage.combat), 2)
        with self.assertRaises(ValueError):
            mage.combat = [5]  # Must be length of 2
        self.assertIsInstance(mage.health, int)
        self.assertIsInstance(mage.temp_health, int)
        self.assertIsInstance(mage.combat, list)
        self.assertIsInstance(mage.move, int)
        self.assertIsInstance(mage.range, int)

        mage.combat = [2, 2]
        mage.health = 5
        mage.temp_health = 5
        mage.move = 2
        mage.range = 3
        self.assertEqual(mage.combat, [2, 2])
        self.assertEqual(mage.health, 5)
        self.assertEqual(mage.temp_health, 5)
        self.assertEqual(mage.move, 2)
        self.assertEqual(mage.range, 3)

    def test_paladin(self):
        paladin = Paladin()
        self.assertEqual(len(paladin.combat), 2)
        with self.assertRaises(ValueError):
            paladin.combat = [5]  # Must be length of 2
        self.assertIsInstance(paladin.health, int)
        self.assertIsInstance(paladin.temp_health, int)
        self.assertIsInstance(paladin.combat, list)
        self.assertIsInstance(paladin.move, int)
        self.assertIsInstance(paladin.range, int)

        paladin.combat = [3, 3]
        paladin.health = 6
        paladin.temp_health = 6
        paladin.move = 3
        paladin.range = 1
        self.assertEqual(paladin.combat, [3, 3])
        self.assertEqual(paladin.health, 6)
        self.assertEqual(paladin.temp_health, 6)
        self.assertEqual(paladin.move, 3)
        self.assertEqual(paladin.range, 1)

    def test_ranger(self):
        ranger = Ranger()
        self.assertEqual(len(ranger.combat), 2)
        with self.assertRaises(ValueError):
            ranger.combat = [5]  # Must be length of 2
        self.assertIsInstance(ranger.health, int)
        self.assertIsInstance(ranger.temp_health, int)
        self.assertIsInstance(ranger.combat, list)
        self.assertIsInstance(ranger.move, int)
        self.assertIsInstance(ranger.range, int)

        ranger.combat = [3, 3]
        ranger.health = 5
        ranger.temp_health = 5
        ranger.move = 3
        ranger.range = 3
        self.assertEqual(ranger.combat, [3, 3])
        self.assertEqual(ranger.health, 5)
        self.assertEqual(ranger.temp_health, 5)
        self.assertEqual(ranger.move, 3)
        self.assertEqual(ranger.range, 3)

    def test_hero_warrior_attack_goblin_bonus(self):
        warrior = Warrior()
        goblin = Goblin()
        result = warrior.calculate_dice(goblin, True, [1, 6], [1, 6])
        expected = 1
        self.assertEqual(result, expected)

    def test_necromancer_raise_dead(self):
        necro = Necromancer()
        goblin = Goblin()
        goblin.temp_health = 0
        from_coord = Coord(1, 1)
        to_coord = Coord(1, 2)
        board = [[None for _ in range(5)] for _ in range(5)]
        board[1][2] = goblin
        necro.raise_dead(goblin, from_coord, to_coord, board)
        self.assertEqual(goblin.player, Player.VILLAIN)

    def test_necromancer_cannot_raise_alive_target(self):
        self.goblin.temp_health = 1  # Goblin "alive"
        initial_health = self.goblin.temp_health

        from_coord = Coord(1, 1)
        to_coord = Coord(1, 2)
        self.necromancer.raise_dead(self.goblin, from_coord, to_coord, self.board)
        self.assertEqual(self.goblin.temp_health, initial_health)

    def test_paladin_revive_dead_target(self):
        self.goblin.temp_health = 0
        from_coord = Coord(1, 1)
        to_coord = Coord(1, 2)
        self.paladin.revive(self.goblin, from_coord, to_coord, self.board)
        self.assertEqual(self.goblin.temp_health, self.goblin.health // 2)
        self.assertFalse(self.paladin.heal)  # Heal ability used

    def test_paladin_cannot_revive_alive_target(self):
        self.goblin.temp_health = 2  # Not "dead"
        initial_health = self.goblin.temp_health

        from_coord = Coord(1, 1)
        to_coord = Coord(1, 2)
        self.paladin.revive(self.goblin, from_coord, to_coord, self.board)
        self.assertEqual(self.goblin.temp_health, initial_health)

    def test_paladin_revive(self):
        paladin = Paladin()
        goblin = Goblin()
        goblin.temp_health = 0
        from_coord = Coord(1, 1)
        to_coord = Coord(1, 2)
        board = [[None for _ in range(5)] for _ in range(5)]
        paladin.revive(goblin, from_coord, to_coord, board)
        self.assertEqual(goblin.temp_health, goblin.health // 2)

    def test_warrior_attack_dice(self):
        attack_rolls = [5, 6, 2, 3]
        successful_rolls = self.warrior.calculate_dice(target=self.goblin, attack=True, lst=attack_rolls)
        self.assertEqual(successful_rolls, 2)  # Two rolls meet the success criteria

    def test_ranger_deal_damage(self):
        self.ranger.deal_damage(self.skeleton, 3)
        self.assertEqual(self.skeleton.temp_health, self.skeleton.health - 2)  # Skeleton takes reduced damage

    def test_mage_deal_damage(self):
        self.mage.deal_damage(self.warrior, 2)
        self.assertEqual(self.warrior.temp_health, self.warrior.health - 3)  # Mage deals +1 damage

    def test_goblin_invalid_move_out_of_range(self):
        from_coord = Coord(0, 0)
        to_coord = Coord(4, 0)
        self.assertFalse(self.goblin.is_valid_move(from_coord, to_coord, self.board))

    def test_skeleton_valid_diagonal_move(self):
        from_coord = Coord(1, 1)
        to_coord = Coord(1, 3)
        self.board[1][1] = self.skeleton
        self.assertTrue(
            self.skeleton.is_valid_move(from_coord, to_coord, self.board))  # Only horizontal/vertical allowed

    def test_skeleton_damage_reduction(self):
        initial_health = self.skeleton.temp_health
        self.ranger.deal_damage(self.skeleton, 3)
        self.assertEqual(self.skeleton.temp_health, initial_health - 2)  # 1 point less

    def test_goblin_combat_roll(self):
        goblin = Goblin()
        roll1 = [2, 5, 4]
        result1 = goblin.calculate_dice(attack=True, lst=roll1)
        self.assertEqual(result1, 1)  # Only one roll should meet the criteria

        roll2 = [2, 5, 4]
        result2 = goblin.calculate_dice(attack=False, lst=roll2)
        self.assertEqual(result2, 2)

    def test_warrior_resets_attack_bonus_after_combat(self):
        attack_rolls = [5, 6]
        self.warrior.calculate_dice(self.goblin, True, attack_rolls)
        self.assertEqual(self.warrior.combat[0], 2)  # Warrior's attack should reset

    def test_paladin_range_limits_revive(self):
        # Revive should not work out of range
        self.goblin.temp_health = 0
        from_coord = Coord(0, 0)
        to_coord = Coord(4, 4)
        self.paladin.revive(self.goblin, from_coord, to_coord, self.board)
        self.assertEqual(self.goblin.temp_health, 0)  # Should not revive due to range

    def test_ranger_attack_outside_range(self):
        # Ensures Ranger cannot attack if out of range
        from_coord = Coord(0, 0)
        to_coord = Coord(4, 4)
        self.assertFalse(self.ranger.is_valid_attack(from_coord, to_coord, self.board))


# Testing Dungeon Functionality

class TestDungeon(unittest.TestCase):

    def setUp(self):
        # Basic setup with a small dungeon
        self.dungeon = Dungeon(6, 6)

    def test_dungeon_init(self):
        dungeon = Dungeon(6, 6)
        self.assertEqual(dungeon.height, 6)
        self.assertEqual(dungeon.width, 6)
        self.assertEqual(len(dungeon.board), 6)
        self.assertTrue(all(len(row) == 6 for row in dungeon.board))

        # Test correct dungeon size setup
        self.assertEqual(self.dungeon.height, 6)
        self.assertEqual(self.dungeon.width, 6)
        self.assertIsInstance(self.dungeon.board, list)
        self.assertEqual(len(self.dungeon.board), 6)
        self.assertEqual(len(self.dungeon.board[0]), 6)

    def test_dungeon_invalid_dimensions(self):
        # Test invalid dimensions raise ValueError
        with self.assertRaises(ValueError):
            Dungeon(3, 6)  # Height too small
        with self.assertRaises(ValueError):
            Dungeon(6, 13)  # Width too large

    def test_dungeon_villains_initialization(self):
        # Verify villains are generated if none provided
        dungeon = Dungeon(6, 6)
        self.assertGreaterEqual(len(dungeon.villains), 1)

    def test_hero_initialization(self):
        # Check hero team initialization
        heroes = self.dungeon.heroes
        self.assertEqual(len(heroes), 4)
        self.assertIsInstance(heroes[0], Warrior)
        self.assertIsInstance(heroes[1], Mage)
        self.assertIsInstance(heroes[2], Paladin)
        self.assertIsInstance(heroes[3], Ranger)

    def test_set_board(self):
        # Test setting board with a list resets the board, otherwise raises TypeError
        dungeon = Dungeon(6, 6)
        new_board = [[None] * 6 for _ in range(6)]
        dungeon.board = new_board
        self.assertEqual(dungeon.board, new_board)

        with self.assertRaises(TypeError):
            dungeon.board = "Invalid Board"  # Not a list

    def test_villain_generation(self):
        # Test villain generation
        self.dungeon.generate_villains()
        villains = self.dungeon.villains
        self.assertTrue(len(villains) >= 1)
        self.assertTrue(all(isinstance(villain, Villain) for villain in villains))

    def test_place_heroes(self):
        # Test placing heroes on the board
        self.dungeon.place_heroes()
        middle = self.dungeon.width // 2
        self.assertIsInstance(self.dungeon.character_at(self.dungeon.height - 2, middle - 1), Warrior)

    def test_place_villains(self):
        # Test placing villains on the board
        self.dungeon.generate_villains()
        self.dungeon.place_villains()
        for villain in self.dungeon.villains:
            found = any(villain in row for row in self.dungeon.board)
            self.assertTrue(found)

    def test_move_character(self):
        dungeon = Dungeon(6, 6)
        warrior = Warrior()
        from_coord = Coord(0, 0)
        to_coord = Coord(1, 1)
        dungeon.set_character_at(warrior, from_coord.x, from_coord.y)
        dungeon.move(from_coord, to_coord)
        self.assertEqual(dungeon.character_at(to_coord.x, to_coord.y), warrior)
        self.assertIsNone(dungeon.character_at(from_coord.x, from_coord.y))

        hero = Warrior()
        self.dungeon.set_character_at(hero, 4, 2)
        self.dungeon.move(Coord(4, 2), Coord(3, 2))
        self.assertIsNone(self.dungeon.character_at(4, 2))
        self.assertEqual(self.dungeon.character_at(3, 2), hero)

    def test_is_valid_move_within_bounds(self):
        # Test move validity within board bounds
        self.assertTrue(self.dungeon.is_valid_move([Coord(1, 1), Coord(2, 1)]))

    def test_is_valid_move_out_of_bounds(self):
        # Test move validity outside board bounds
        self.assertFalse(self.dungeon.is_valid_move([Coord(5, 5), Coord(7, 7)]))

    def test_is_valid_attack(self):
        # Test attack validity (valid case)
        attacker = Mage()
        target = Goblin()
        self.dungeon.set_character_at(attacker, 3, 3)
        self.dungeon.set_character_at(target, 4, 3)
        self.assertTrue(self.dungeon.is_valid_attack([Coord(3, 3), Coord(4, 3)]))

    def test_invalid_attack_out_of_bounds(self):
        # Test invalid attack (out of bounds)
        self.assertFalse(self.dungeon.is_valid_attack([Coord(1, 1), Coord(7, 7)]))

    def test_toggle_player(self):
        # Test player toggle between HERO and VILLAIN
        initial_player = self.dungeon.player
        self.dungeon.set_next_player()
        self.assertNotEqual(self.dungeon.player, initial_player)

    def test_board_generation(self):
        # Test board generation with a new size
        self.dungeon.generate_new_board(8, 8)
        self.assertEqual(self.dungeon.height, 8)
        self.assertEqual(self.dungeon.width, 8)
        self.assertEqual(len(self.dungeon.board), 8)
        self.assertEqual(len(self.dungeon.board[0]), 8)

    def test_character_at_valid(self):
        # Test retrieving character at a valid position
        hero = Warrior()
        self.dungeon.set_character_at(hero, 1, 1)
        self.assertEqual(self.dungeon.character_at(1, 1), hero)

    def test_character_at_out_of_bounds(self):
        # Test retrieving character at out-of-bounds position
        with self.assertRaises(ValueError):
            self.dungeon.character_at(10, 10)

    def test_set_character_out_of_bounds(self):
        # Test placing character out of bounds
        with self.assertRaises(ValueError):
            self.dungeon.set_character_at(Warrior(), 10, 10)

    def test_heroes_defeat(self):
        # Test if all heroes are defeated
        for hero in self.dungeon.heroes:
            hero.temp_health = 0
        self.assertTrue(self.dungeon.adventurer_defeat())

    def test_dungeon_clear(self):
        # Test if all villains are defeated
        villains = [Goblin(), Skeleton(), Necromancer()]
        self.dungeon._Dungeon__villains = villains
        for villain in villains:
            villain.temp_health = 0
        self.assertFalse(self.dungeon.is_dungeon_clear())

    def test_print_board(self):
        # Simply check if print_board runs without error (visual inspection required)
        try:
            self.dungeon.print_board()
        except Exception as e:
            self.fail(f"print_board() raised an exception: {e}")


if __name__ == '__main__':
    unittest.main()
