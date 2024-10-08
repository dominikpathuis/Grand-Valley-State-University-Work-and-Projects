# Dominik Pathuis

# This code works as a simulation for the Mega Millions Lottery.

# I certify that this code is mine, and mine alone, in accordance with GVSU academic honesty policy.

# Completed April 16, 2024

class LotteryTicket:
    def __init__(self, info):
        # Split the info string into multiple pieces separated by ','
        tokens = info.split(',')

        # Assigning values to instance variables after stripping extra spaces
        self.first = tokens[0].strip()
        self.last = tokens[1].strip()
        self.city = tokens[2].strip()
        self.state = tokens[3].strip()
        self.zipcode = int(tokens[4].strip())

        # Strip the full birthday and then extract the day, month, year
        birthday = tokens[5].strip()
        pieces = birthday.split('/')
        self.day = int(pieces[1])
        self.month = int(pieces[0])
        self.year = int(pieces[2])

        # Extract the lottery numbers and convert them to integers
        # Extract the mega ball number
        self.mega_ball = int(tokens[11].strip())

        # Returns a list of the 5 numbers selected
        self.nums = []
        for num in tokens[6:11]:
            self.nums.append(int(num.strip()))

        # Set initial prize to 0
        self.prize = 0

    # Getters for various ticket information
    def get_first(self):
        return self.first

    def get_last(self):
        return self.last

    def get_city(self):
        return self.city

    def get_state(self):
        return self.state

    def get_zipcode(self):
        return self.zipcode

    def get_day(self):
        return self.day

    def get_month(self):
        return self.month

    def get_year(self):
        return self.year

    def get_prize(self):
        return self.prize

    def get_mega_ball(self):
        return self.mega_ball

    def get_nums(self):
        return self.nums

    def has_ball(self, val):
        if val in self.nums:
            return True
        return False

    # Check if the ticket has a particular number or mega ball
    def has_mega_ball(self, val):
        if val == self.mega_ball:
            return True
        return False

    # String representation of the ticket
    def __str__(self):
        numbers_str = ''
        for num in self.nums:
            numbers_str += str(num) + ' '

        numbers_str = numbers_str.strip()

        return (f'{self.first} {self.last}\n{self.city}, {self.state} {self.zipcode}\n{numbers_str}    '
                f'{self.mega_ball}\nPrize: ${self.prize:.2f}')

    # Setter for prize amount
    def set_prize(self, amount):
        self.prize = amount


if __name__ == '__main__':
    t = LotteryTicket("Louis,Laker,Allendale,MI,49401,4/20/1985,5,10,15,20,25,7")
    print(t)








from lottery_ticket import LotteryTicket
import random


class LotteryMachine:
    # Initialize lists to hold lottery tickets and drawn numbers
    def __init__(self):
        self.lottery_tickets = []
        self.lottery_numbers = []
        self.mega_ball = None

    # Getters for ticket count, drawn numbers, and mega ball
    def get_ticket_count(self):
        return len(self.lottery_tickets)

    def get_mega_ball(self):
        return self.mega_ball

    def get_nums(self):
        return self.lottery_numbers

    # Method to add a ticket to the machine
    def add_ticket(self, t):
        return self.lottery_tickets.append(t)

    # Method to read tickets from a file and add them to the machine
    def read_tickets(self, filename):
        file = open(filename)
        for entry in file:
            t = LotteryTicket(entry)
            self.add_ticket(t)
        file.close()

    # Method to draw random numbers for the lottery
    def draw_random_numbers(self):
        # Select five random numbers without duplicates between 1 and 75
        self.lottery_numbers = random.sample(range(1, 76), 5)
        # Select a random mega ball number between 1 and 15
        self.mega_ball = random.randint(1, 15)

    # Method to count the number of matches between a ticket and drawn numbers
    def count_matches(self, t):
        matches = 0
        ticket_numbers = t.get_nums()
        drawn_numbers = self.get_nums()

        # Iterate through the ticket numbers
        for number in ticket_numbers:
            # Check if the number is among the drawn numbers
            if number in drawn_numbers:
                matches += 1

        return matches

    # Method to assign prize amounts to tickets based on matches
    def make_payouts(self):
        for ticket in self.lottery_tickets:
            matches = self.count_matches(ticket)
            has_mega_ball = ticket.has_mega_ball(self.mega_ball)
            if matches == 5:
                if has_mega_ball:
                    ticket.set_prize(5000000)
                else:
                    ticket.set_prize(1000000)
            elif matches == 4:
                if has_mega_ball:
                    ticket.set_prize(5000)
                else:
                    ticket.set_prize(500)
            elif matches == 3:
                if has_mega_ball:
                    ticket.set_prize(50)
                else:
                    ticket.set_prize(5)
            elif matches == 2:
                if has_mega_ball:
                    ticket.set_prize(5)
                else:
                    ticket.set_prize(0)
            elif matches == 1:
                if has_mega_ball:
                    ticket.set_prize(2)
                else:
                    ticket.set_prize(0)
            elif matches == 0:
                if has_mega_ball:
                    ticket.set_prize(1)
                else:
                    ticket.set_prize(0)

    # String representation of the drawn numbers
    def __str__(self):
        numbers_str = ' '.join(str(num) for num in self.lottery_numbers)
        selected_numbers_str = f"Selected Numbers: {numbers_str} {self.mega_ball}"
        return selected_numbers_str

    # Method to simulate drawing a ticket
    def draw_ticket(self):
        self.draw_random_numbers()
        self.make_payouts()

    # Method to simulate drawing a ticket with specific numbers for testing purposes
    def test_ticket(self, b1, b2, b3, b4, b5, mega):
        # Assign parameters to the six lottery numbers
        self.lottery_numbers = [b1, b2, b3, b4, b5]
        self.mega_ball = mega

        # Call make_payouts to assign awards
        self.make_payouts()

    # Method to print a report for tickets sold in a specific state
    def print_report(self, st):
        # Initialize variables to store ticket count, total prize amount, and the biggest winner
        ticket_count = 0
        total_prize = 0
        biggest_winner = None

        # Iterate through all tickets and calculate total prize amount and find the biggest winner
        for ticket in self.lottery_tickets:
            if ticket.get_state() == st:
                ticket_count += 1
                total_prize += ticket.get_prize()
                if biggest_winner is None or ticket.get_prize() > biggest_winner.get_prize():
                    biggest_winner = ticket

        # Check if no tickets were sold in the state
        if ticket_count == 0:
            print(f"No tickets were sold in {st}")
            return 0

        # Calculate the average prize amount
        average_prize = total_prize / ticket_count

        # Print the report
        print(f"Report for {st}")
        print(f"Winning Numbers: {self}")
        print(f"Tickets sold: {ticket_count}")
        print(f"Average prize: ${average_prize:.2f}")

        # Check if there is a biggest winner and print their details
        if biggest_winner is not None:
            print("\nBiggest Winner")
            print(biggest_winner)

        return ticket_count

    # Method to find the oldest player based on birth date
    def get_oldest_player(self):
        oldest_ticket = None
        oldest_birth_date = None

        for ticket in self.lottery_tickets:
            birth_day = ticket.get_day()
            birth_month = ticket.get_month()
            birth_year = ticket.get_year()

            # Calculate age based on current date
            age = 2024 - birth_year
            if 4 < birth_month or (birth_month == 4 and birth_day > 16):
                age -= 1

            # Check if this ticket is the oldest so far
            if oldest_birth_date is None or age > oldest_birth_date:
                oldest_ticket = ticket
                oldest_birth_date = age

        return oldest_ticket

    # Method to find the ticket with the largest prize
    def get_big_winner(self):
        # Initialize variables to store the ticket with the largest prize and the largest prize amount
        big_winner_ticket = None
        largest_prize = 0

        # Iterate through all tickets
        for ticket in self.lottery_tickets:
            # Get the prize of the current ticket
            ticket_prize = ticket.get_prize()

            # Check if the current ticket has a larger prize than the current largest prize
            if ticket_prize > largest_prize:
                big_winner_ticket = ticket
                largest_prize = ticket_prize

        # Return the ticket with the largest prize
        return big_winner_ticket

    # Method to find all tickets with a prize amount greater than or equal to a specified amount
    def get_big_winners(self, amount):
        big_winners = []
        for ticket in self.lottery_tickets:
            if ticket.get_prize() >= amount:
                big_winners.append(ticket)
        return big_winners

    # Method to print all big winners with a prize amount greater than or equal to a specified amount
    def print_big_winners(self, amount):
        # Get the list of big winners
        big_winners = self.get_big_winners(amount)

        # Print the heading
        print("Big Winners ($50 or higher)\n")

        # Iterate through the list of big winners
        for ticket in big_winners:
            # Print ticket information
            print(ticket)

        # Print the total number of winning tickets
        print(f"{len(big_winners)} winning tickets")

    # Method to simulate multiple drawings of the lottery
    def multiple_drawings(self, num):
        jackpot_amount = 5000000
        has_mega_winner = False
        largest_prize = 500
        big_winner_info = ""

        for i in range(num):
            # Draw ticket
            self.draw_ticket()

            # Check if there's a Mega Millions winner
            if self.count_matches(self.get_big_winner()) == 5 and self.get_big_winner().has_mega_ball(
                    self.get_mega_ball()):
                has_mega_winner = True
                break

            # Update jackpot amount
            jackpot_amount += 1500000

            # Check if current prize is the largest
            if self.get_big_winner().get_prize() > largest_prize:
                largest_prize = self.get_big_winner().get_prize()
                big_winner_info = self.get_big_winner().__str__()

        # Print the number of drawings
        print(f"Number of drawings: {i + 1}")

        # Print the biggest winner
        print(big_winner_info)

        # Return the largest prize value
        return largest_prize




if __name__ == '__main__':
    lm = LotteryMachine()
    lm.read_tickets("ticket_info.txt")
    print(lm.multiple_drawings(100))


