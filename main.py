'''
Main logic for the blackjack game. Keeping it simple, no splits, doubles, etc.
Dealer must hit until 17.
Cards dealt face up to player, one up one down to Dealer.
One deck, shuffled after each hand.
2:1 payout.
Ace = 11 for now
'''
import time
from bj_classes import Deck, Player


def buy_in():
    '''
    Initial buy in. Might allow players to buy back in in the future.
    Verifies that buy in is an int between a specified range.
    '''
    while True:
        try:
            user_input = int(input("How many chips would you like to buy in with? "))
            if user_input not in range(1,10000001):
                print("Sorry, you can only buy in with 1-10M chips at this table.")
                continue
        except ValueError:
            print("Please enter chip amount as a whole number.")
            continue
        print(f"Thank you, {player_one.name}. You have deposited {user_input} chips.\n")
        return user_input

def place_bet():
    '''
    Asks for a user bet. Verifies that they have enough to cover and it's an int > 0
    Remove the chip amount from their total and return the current bet amount.
    '''
    print(player_one)
    while True:
        try:
            user_bet = int(input("How many chips would you like to bet? "))
            if user_bet > player_one.chips:
                print("Sorry, you don't have that many chips.")
                print('')
                continue
            if user_bet < 1:
                print("You must bet at least one chip.")
                print('')
                continue
        except ValueError:
            print("Please enter chip amount as a whole number.")
            continue
        player_one.remove_chips(user_bet)
        print(player_one)
        return user_bet

def blackjack_check(hand):
    '''
    Takes a hand and sees if we hit 21. Returns bool
    '''
    if hand[0].value + hand[1].value == 21:
        return True
    return False

def player_choice():
    '''
    Get a player choice. Verify it is either hit or stand.
    '''
    while True:
        choice = input("Would you like to hit or stand? ").upper()

        if choice in ('HIT','H','HIT ME','BIG HIT','BADA BING BADA BOOM'):
            return 'HIT'
        if choice in ('STAND','S','ST','HOLD','CHILL'):
            return 'STAND'
        print("Invalid input.")
        continue

def player_continue():
    '''
    Ask the player if they want to continue. Return bool
    '''
    if player_one.chips < 1:
        print(f"Sorry {player_one.name}, you are out of chips!")
        return False
    while True:
        choice = input("Would you like to play again? ").upper()

        if choice in ('YES','Y','YA','YESSIR'):
            return True
        if choice in ('NO','N','NAH','NOSIR','NO SIR','NO MAAM'):
            return 'STAND'
        print("Please enter Yes or No.")
        continue

def who_wins(p_hand,d_hand):
    '''
    Determine who wins. Add chips if necessary.
    '''
    player_hand_tot = 0
    dealer_hand_tot = 0

    print(f"\n{player_one.name}, you have the following cards: ")
    for p_card in p_hand:
        print(p_card)
        player_hand_tot += p_card.value
    print(f"Your card total is {player_hand_tot}\n")
    time.sleep(2)
    print("The Dealer has the following cards: ")
    for d_card in d_hand:
        print(d_card)
        dealer_hand_tot += d_card.value
    print(f"The Dealer's card total is {dealer_hand_tot}\n")

    if dealer_hand_tot > 21:
        print(f"The Dealer busts! {player_one.name} WINS {CURRENT_BET} CHIPS!")
        player_one.add_chips(CURRENT_BET * 2)
    elif player_hand_tot > dealer_hand_tot:
        print(f"{player_one.name} WINS {CURRENT_BET} CHIPS!")
        player_one.add_chips(CURRENT_BET * 2)
    elif dealer_hand_tot > player_hand_tot:
        print(f"The dealer wins {CURRENT_BET} chips from {player_one.name}...")
    else:
        print(f"It was a push... {player_one.name}, you get your {CURRENT_BET} chips back.")
        player_one.add_chips(CURRENT_BET)

def pull_dealer_cards(d_hand):
    '''
    Pulls cards for the dealer until they get at least 17
    '''
    while True:
        running_total = 0
        for crd in d_hand:
            running_total += crd.value
        if running_total >= 17:
            return d_hand
        d_hand.append(deck_one.all_cards.pop())
        continue

# Variables we may need
GAME_ON = True
HAND_COUNT = 0

# Get the player name
player_one = Player(input("Please enter your name: "))

# How many chips did the player bring?
player_one.add_chips(buy_in())

# GAME LOGIC
#
while GAME_ON:

    # Game variables that will reset with each hand
    CURRENT_BET = 0

    player_hand = []
    PLAYER_HAND_TOTAL = 0
    dealer_hand = []
    DEALER_HAND_TOTAL = 0

    PLAYER_CAN_CHOOSE = True
    NEED_TO_CHECK_CARDS = True

    # Let's keep track of how many hands we've played
    HAND_COUNT += 1
    if HAND_COUNT == 1:
        print(f"Welcome to the table, {player_one.name}. Best of luck to you.\n")
    else:
        print(f"\nIt is now hand #{HAND_COUNT}\n")

    # First let's get our bet
    CURRENT_BET = place_bet()

    # Second let's generate a new deck object and shuffle it
    time.sleep(1)
    deck_one = Deck()
    deck_one.shuffle_cards()
    time.sleep(1)

    # Now let's deal the cards, starting with the player
    #
    print("Dealing the cards...\n")
    time.sleep(2)
    for x in range(0,2):
        player_hand.append(deck_one.all_cards.pop())
        dealer_hand.append(deck_one.all_cards.pop())

    print(f"{player_one.name}, you were dealt the {player_hand[0]} and the {player_hand[1]}")
    print(f"The dealer is showing the {dealer_hand[-1]}\n")

    # If they hit blackjack, no need to continue
    if blackjack_check(player_hand):
        PLAYER_CAN_CHOOSE = False
        print(f"{player_one.name} HIT BLACKJACK!!")
        print(f"The dealer has the {dealer_hand[0]} and the {dealer_hand[1]}.")

        if blackjack_check(dealer_hand):
            print("The dealer also hit Blackjack... It's a push.")
            print(f"{player_one.name} gets {CURRENT_BET} chips back.")
            player_one.add_chips(CURRENT_BET)
            break
        player_one.add_chips(CURRENT_BET * 2)
        print(f"{player_one.name} won {CURRENT_BET} chips with 21!")
        NEED_TO_CHECK_CARDS = False

    # Betting loop
    while PLAYER_CAN_CHOOSE:

        PLAYER_HAND_TOTAL = 0
        DEALER_HAND_TOTAL = 0

        # Get the player's choice
        PLAYER_CHOICE_INPUT = player_choice()
        print(f"\nYou chose to {PLAYER_CHOICE_INPUT}.")
        time.sleep(1)

        # They stand. Break and compare
        if PLAYER_CHOICE_INPUT == 'STAND':
            PLAYER_CAN_CHOOSE = False
            NEED_TO_CHECK_CARDS = True
            break

        # They hit. Deal new card and check if they bust or get 21
        # If neither, let them choose again
        player_hand.append(deck_one.all_cards.pop())
        print(f"You were dealt the {player_hand[-1]}\n")
        print("You now have the following cards in your hand: ")

        # Take total value of cards, show the player what they have
        PLAYER_HAND_TOTAL = 0
        for card in player_hand:
            print(card)
            PLAYER_HAND_TOTAL += card.value
        print(f"Your hand total is {PLAYER_HAND_TOTAL}\n")
        time.sleep(2)

        # Check for 21 or bust
        if PLAYER_HAND_TOTAL == 21:
            PLAYER_CAN_CHOOSE = False
            NEED_TO_CHECK_CARDS = True
            print("You now have 21! Let's see what the dealer gets...")
            break
        if PLAYER_HAND_TOTAL > 21:
            PLAYER_CAN_CHOOSE = False
            NEED_TO_CHECK_CARDS = False
            print(f"Sorry, {player_one.name}. You bust with a total of {PLAYER_HAND_TOTAL}...")
            break
        continue

    if NEED_TO_CHECK_CARDS is True:
        dealer_hand = pull_dealer_cards(dealer_hand)
        who_wins(player_hand,dealer_hand)

    # Verify the player has chips left, then ask if they want to continue
    print(f"You have {player_one.chips} chips remaining.")
    GO_AGAIN = player_continue()
    if GO_AGAIN is True:
        continue
    GO_AGAIN = False
    break

print("Thank you for playing.")
