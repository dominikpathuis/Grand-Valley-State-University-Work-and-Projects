# Dominik Pathuis

# This code calculates airfare based on day, destination, row #, checked bags, and optional Premium Plus

# I certify that this code is mine, and mine alone, in accordance with GVSU academic honesty policy.

# Completed February 3, 2024

# Importing sys allows for use of the exit() function

import sys

# Input is received from the user

destination = input()
day = input()
row = int(input())
bags = int(input())
premium_plus = input()

# The if statement prompts the user for a premium plus selection

if premium_plus == 'y':
    premium_plus = True
elif premium_plus == 'n':
    premium_plus = False

# I set these to 0 so that they are defined and prevents errors

fare = 0
baggage_fee = 0

# Different outputs depending on if the user selects premium plus or not

if premium_plus:
    print(f'Enter information \nDestination: {destination}\nDay: {day}\nRow: {row}\nBags: {bags}\n'
          f'Premium Plus (y/n): y')
else:
    print(f'Enter information \nDestination: {destination}\nDay: {day}\nRow: {row}\nBags: {bags}\n'
          f'Premium Plus (y/n): n')

# Sets the day to Monday by default if the input is invalid

if not (day == 'Mon' or day == 'Tue' or day == 'Wed' or day == 'Thu' or day == 'Fri' or day == 'Sat' or day == 'Sun'):
    day = 'Mon'

# The if statement prevents the program from continuing if an invalid destination is entered

if (destination != 'DFW' and destination != 'LAX' and destination != 'SEA' and destination != 'MIA' and destination !=
        'BOS'):
    print('Oops! Destination must be DFW, LAX, SEA, MIA or BOS.')
    sys.exit()
else:

    # The following if statement blocks output the fare amount for each destination on a given day

    if day == 'Mon' or day == 'Thu':    # Fares for Mon and Thu are the same
        if destination == 'DFW':
            fare = 213.00
        elif destination == 'LAX':
            fare = 334.00
        elif destination == 'MIA':
            fare = 279.00
        elif destination == 'SEA':
            fare = 315.00
        elif destination == 'BOS':
            fare = 241.00

    elif day == 'Tue' or day == 'Wed':    # Fares for Tue and Wed are the same
        if destination == 'DFW':
            fare = 198.00
        elif destination == 'LAX':
            fare = 314.00
        elif destination == 'MIA':
            fare = 204.00
        elif destination == 'SEA':
            fare = 294.00
        elif destination == 'BOS':
            fare = 205.00


    elif day == 'Fri':
        if destination == 'DFW':
            fare = 399.00
        elif destination == 'LAX':
            fare = 429.00
        elif destination == 'MIA':
            fare = 370.00
        elif destination == 'SEA':
            fare = 430.00
        elif destination == 'BOS':
            fare = 298.00

    elif day == 'Sat':
        if destination == 'DFW':
            fare = 213.00
        elif destination == 'LAX':
            fare = 334.00
        elif destination == 'MIA':
            fare = 279.00
        elif destination == 'SEA':
            fare = 315.00
        elif destination == 'BOS':
            fare = 241.00

    elif day == 'Sun':
        if destination == 'DFW':
            fare = 198.00
        elif destination == 'LAX':
            fare = 314.00
        elif destination == 'MIA':
            fare = 204.00
        elif destination == 'SEA':
            fare = 294.00
        elif destination == 'BOS':
            fare = 205.00

# The if statement prevents the program from continuing if an invalid row is entered

if row < 1 or row > 35:
    print('Oops! Row must be 1 - 35.')
    sys.exit()

# Adjusts fare and baggage fee if Premium Plus is selected

if premium_plus:
    fare += 94.00  # Additional fare for Premium Plus
    if bags < 0:
        bags = 0  # Ensure bags don't go negative
    elif bags == 1:
        baggage_fee = 0  # Free checked bag with premium plus
    elif bags == 2:
        baggage_fee = 35.00
    elif bags >= 3:
        baggage_fee = (bags - 1) * 25.00

# Adjust fare for premium plus and first class

if premium_plus:
    if row <= 7:
        fare = (fare * 0.75) + fare

# This if statement block adjusts the fare amount with additional fees depending on the row

if not premium_plus:
    if row <= 7:
        first_class_rate = (fare * 0.75) + fare     # first class adds a 75% charge to the fare
        fare = first_class_rate
    elif row == 14 or row == 15:                    # exit rows add a $49 fee because of the extra legroom
        exit_row_rate = fare + 49
        fare = exit_row_rate
    elif (row <= 20 and row >= 16) or (row <= 13 and row >= 8):     # preferred seats add an extra fee of $35
        preferred_seat_rate = fare + 35
        fare = preferred_seat_rate

# this if statement block calculates baggage fees for non-premium plus flyers

if not premium_plus:
    if bags == 1:
        baggage_fee = 35.00                   # $35 for first checked bag
    elif bags > 1:
        baggage_fee = (bags * 25.00) + 10.00  # $25 for any additional bag

# 18% tax rate. But baggage fee is not taxed

tax_rate = 0.18
taxes = fare * tax_rate
total = fare + taxes + baggage_fee

# This if statement outputs the price breakdown and total from all inputted information

if premium_plus:
    taxes = (fare + 94.00) * tax_rate
    print(f'Ticket Price Summary\nFare: ${fare:.2f}\nBags: ${baggage_fee:.2f}\nPremium: $94.00\nTaxes: '
          f'${taxes:.2f}\nTotal: ${total:.2f}')
else:
    print(f'Ticket Price Summary\nFare: ${fare:.2f}\nBags: ${baggage_fee:.2f}\nTaxes: ${taxes:.2f}\nTotal: '
          f'${total:.2f}')



