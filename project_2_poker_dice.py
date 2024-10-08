# Dominik Pathuis

# This code provides support for the scorecard of a poker dice game.

# I certify that this code is mine, and mine alone, in accordance with GVSU academic honesty policy.

# Completed March 19, 2024


# Each scoring category is defined using all caps to ensure the value does not change.

ONE_PAIR = 10
TWO_PAIR = 20
THREE_OF_A_KIND = 25
SMALL_STRAIGHT = 30
FULL_HOUSE = 35
FOUR_OF_A_KIND = 40
LARGE_STRAIGHT = 45
FIVE_OF_A_KIND = 50


# This function creates a list with seven zeros that will tally the counts of each number from 1 to 6 and
# update the tally based on the values of the dice

def tally_dice(dice):
    tally = [0] * 7

    # Count occurrences of each number in dice

    for value in dice:
        tally[value] += 1

    return tally


# This function determines if a straight of specified length exists in the dice

def has_straight(length, dice):
    tally = tally_dice(dice)

    # Check for consecutive numbers in the tally to look for a straight

    for i in range(1, 7 - length + 1):
        straight_found = True
        for j in range(length):
            if tally[i + j] == 0:
                straight_found = False
                break
        if straight_found:
            return True

    return False


# Function to check if there are 'count' or more identical values in the dice

def has_multiples(count, dice):
    tally = tally_dice(dice)

    # Check if any count in the tally is greater than or equal to 'count'. That means there is a multiple

    for value_count in tally:
        if value_count >= count:
            return True

    return False


# The following functions are defining the scoring categories

# Check for five of a kind

def five_of_kind(dice):
    return has_multiples(5, dice)


# Check for four of a kind

def four_of_kind(dice):
    return has_multiples(4, dice)


# Check for three of a kind

def three_of_kind(dice):
    return has_multiples(3, dice)


# Check for a full house

def full_house(dice):
    counts = {}
    for value in dice:
        counts[value] = counts.get(value, 0) + 1

    return (3 in counts.values() and 2 in counts.values()) or (5 in counts.values())


# Check for one pair

def one_pair(dice):
    return has_multiples(2, dice)


# Check for a two pair

def two_pair(dice):
    counts = {}
    for value in dice:
        counts[value] = counts.get(value, 0) + 1

    num_pairs = 0
    for count in counts.values():
        if count == 2 or count == 4:
            num_pairs += 1

    # Check for exactly a two pair, a full house, or five of a kind (all technically are a two pair)

    if num_pairs == 2 or full_house(dice) or five_of_kind(dice) or four_of_kind(dice):
        return True

    return False


# Check for a small straight

def small_straight(dice):
    return has_straight(4, dice)


# Check for a large straight

def large_straight(dice):
    return has_straight(5, dice)


# The following primary functions will help to run the application

# Function to read dice values from user input

def read_dice():
    while True:
        user_input = input("Enter the dice values for this round: ").strip().split()

        # Checks if there are exactly five values entered, returning an error message if not

        if len(user_input) != 5:
            print("Error: Please enter exactly five numbers separated by spaces.")
            continue

        # Converting each input to an integer, returning an error message of a non-number or a number
        # not between 1-6 was entered

        dice = []
        valid_input = True
        for num_str in user_input:
            if not num_str.isdigit():
                print("Error: Please enter numeric values only.")
                valid_input = False
                break
            num = int(num_str)
            if not 1 <= num <= 6:
                print("Error: Dice values must be between 1 and 6.")
                valid_input = False
                break
            dice.append(num)

        if valid_input:
            return dice


# Function to scratch the highest category if no match is found

def scratch_highest_category(selected):
    categories = ["five_of_kind", "large_straight", "four_of_kind", "full_house",
                  "small_straight", "three_of_kind", "two_pair", "one_pair"]

    for category in categories:
        if not selected[category]:
            selected[category] = True
            break


# Function to calculate the score based on the dice values

def score_dice(dice_values):
    total_score = 0
    selected = {
        "five_of_kind": False,
        "large_straight": False,
        "four_of_kind": False,
        "full_house": False,
        "small_straight": False,
        "three_of_kind": False,
        "two_pair": False,
        "one_pair": False

    }
    for dice in dice_values:
        round_score = 0

        if five_of_kind(dice) and not selected["five_of_kind"]:
            round_score = FIVE_OF_A_KIND
            selected["five_of_kind"] = True
        elif large_straight(dice) and not selected["large_straight"]:
            round_score = LARGE_STRAIGHT
            selected["large_straight"] = True
        elif four_of_kind(dice) and not selected["four_of_kind"]:
            round_score = FOUR_OF_A_KIND
            selected["four_of_kind"] = True
        elif full_house(dice) and not selected["full_house"]:
            round_score = FULL_HOUSE
            selected["full_house"] = True
        elif small_straight(dice) and not selected["small_straight"]:
            round_score = SMALL_STRAIGHT
            selected["small_straight"] = True
        elif three_of_kind(dice) and not selected["three_of_kind"]:
            round_score = THREE_OF_A_KIND
            selected["three_of_kind"] = True
        elif two_pair(dice) and not selected["two_pair"]:
            round_score = TWO_PAIR
            selected["two_pair"] = True
        elif one_pair(dice) and not selected["one_pair"]:
            round_score = ONE_PAIR
            selected["one_pair"] = True

        else:
            scratch_highest_category(selected)
        total_score += round_score
        print(f"Score: {total_score}")


if __name__ == '__main__':

    # Get the number of rounds from the user

    rounds = int(input("# of rounds: "))
    dice_nums = []

    # Read dice values for each round

    for num_rounds in range(rounds):

        # Call read_dice function to look for errors

        dice_nums.append(read_dice())

        # Calculate and display the score for each round

    score_dice(dice_nums)








