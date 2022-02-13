'''
Class file for Blackjack game
'''
import random

# Suits, ranks, and corresponding values to create Cards and Decks
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = (
    'Two',
    'Three',
    'Four',
    'Five',
    'Six',
    'Seven',
    'Eight',
    'Nine',
    'Ten',
    'Jack',
    'Queen',
    'King',
    'Ace',
)
values = {
    'Two':2,
    'Three':3,
    'Four':4,
    'Five':5,
    'Six':6,
    'Seven':7,
    'Eight':8,
    'Nine':9,
    'Ten':10,
    'Jack':10,
    'Queen':10,
    'King':10,
    'Ace':11,
}

class Card():
    '''
    A simple card from a standard 52 card deck
    '''

    def __init__(self,suit,rank) -> None:
        self.suit = suit
        self.rank = rank
        self.value = values[rank]

    def __str__(self) -> str:
        return self.rank + " of " + self.suit

class Deck():
    '''
    A collection of 52 unique Cards
    '''

    def __init__(self) -> None:
        self.all_cards = []
        for suit in suits:
            for rank in ranks:
                self.all_cards.append(Card(suit,rank))


    def shuffle_cards(self) -> None:
        '''
        Shuffles cards in place
        '''
        print("\nShuffling the deck...\n")
        random.shuffle(self.all_cards)


    def deal_one_card(self) -> Card:
        '''
        Returns one card
        '''
        return self.all_cards.pop()

class Player():
    '''
    Includes player hands, methods to modify the hand, and other hand methods
    '''

    def __init__(self,name) -> None:
        self.name = name
        self.all_cards = []
        self.chips = 0

    def add_chips(self,num):
        '''
        Adds chips to the players total chip count
        '''
        self.chips += num

    def remove_chips(self,num):
        '''
        Adds chips to the players total chip count
        '''
        self.chips -= num

    def add_cards(self,new_cards):
        '''
        Adds cards to the Player's hand. Supports lists or single Card objects
        '''
        if isinstance(new_cards,list):
            # list of multiple card objects
            self.all_cards.extend(new_cards)
        else:
            # single card object
            self.all_cards.append(new_cards)


    def __str__(self) -> str:
        if self.chips == 1:
            return f"{self.name}, you have {self.chips} chip remaining."

        return f"{self.name}, you have {self.chips} chips remaining."

