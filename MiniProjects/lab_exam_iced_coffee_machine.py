import random


class IcedCoffeeMachine:
    def __init__(self, amount):
        self.credit = 0
        self.total_sales = 0
        self.num_cups = amount
        self.price = 1.80

    def get_inventory(self):
        return self.num_cups

    def get_price(self):
        return self.price

    def cancel_purchase(self):
        return self.credit == 0

    def report_status(self):
        print(f'Inventory: {self.num_cups}')
        print(f'Total Sales: ${self.total_sales:.2f}')

    def insert_coin(self, amount):
        if amount == 0.1 or amount == 0.5 or amount == 0.10 or amount == 0.25 or amount == 0.50 or amount == 1:
            self.credit += amount
        else:
            pass

        if self.credit >= self.price:
            print(f'Please...\nMake A Selection')

        if self.credit < self.price:
            print(f'Credit: ${self.credit:.2f}\nPrice: ${self.price:.2f}')

        if self.num_cups == 0:
            print(f'Sorry. Out of Stock.\nPlease try back later.')

    def restock(self, amount):
        inventory = 0

        if amount > 0:
            inventory = self.num_cups
        else:
            pass

        return inventory

    def display_greeting(self):
        if self.num_cups > 0:
            print(f'Iced Coffee!\nPrice: ${self.price:.2f}')
        else:
            print(f'Sorry. Out of Stock.\nPlease try back later.')

    def make_selection(self):
        self.num_cups -= 1
        self.total_sales += self.price
        change = self.credit - self.price

        if self.credit == self.price:
            print(f'Now dispensing...\nYour Iced Coffee')
            self.credit = 0

        if self.credit > self.price:
            print(f'Now Dispensing...\nYour Iced Coffee and your change\nChange Receiving: {change:.2f}')
            self.credit = 0

        if self.credit < self.price:
            print(f'Credit: ${self.credit:.2f}\nPrice: ${self.price:.2f}')


def simulate_sales():
    sim = IcedCoffeeMachine(10)
    for sales in range(random.randrange(10, 31)):
        sim.insert_coin(.1)
        sim.insert_coin(.1)
        sim.insert_coin(.1)
        sim.insert_coin(.25)
        sim.insert_coin(.25)
        sim.insert_coin(1)

        sim.make_selection()
        sim.report_status()


print(simulate_sales())

if __name__ == "__main__":
    machine1 = IcedCoffeeMachine(10)
    machine2 = IcedCoffeeMachine(5)

    print("Initial status of the Coffee Machines:")
    machine1.report_status()
    machine2.report_status()
    print()

    print("Inserting Coins:")
    machine1.insert_coin(0.1)
    machine1.insert_coin(0.5)
    machine1.insert_coin(0.25)
    machine1.insert_coin(1)
    machine1.insert_coin(0.1)
    machine1.insert_coin(0.5)
    machine1.insert_coin(0.1)
    machine1.insert_coin(0.50)
    machine1.insert_coin(0.1)
    machine1.insert_coin(0.1)
    machine1.insert_coin(0.5)
    machine1.insert_coin(0.1)

    machine2.insert_coin(0.1)
    machine2.insert_coin(0.5)
    machine2.insert_coin(2)
    machine2.insert_coin(1)
    machine2.insert_coin(1)

    print()

    print("Display Greetings:")
    machine1.display_greeting()
    machine2.display_greeting()
    print()

    print("Making Selections:")
    machine1.make_selection()
    machine2.make_selection()
    print()

    print("After Selections:")
    machine1.report_status()
    machine2.report_status()
    print()

    print("Canceling Purchase:")
    print(machine1.cancel_purchase())
    print(machine2.cancel_purchase())
    print()

    print("Restocking:")
    machine1.restock(5)
    machine2.restock(0)
    print()

    print("Final status of the MONEY MACHINES:")
    machine1.report_status()
    machine2.report_status()
