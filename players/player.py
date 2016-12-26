"""
Created on Dec 24, 2016

@author: john papa

Copyright 2016 John Papa.  All rights reserved.
This work is licensed under the MIT License.
"""
import click

from cards.hand import Hand


class Player():

    def __init__(self, name, position='Player'):
        self._name = name
        self._position = position
        self._hand = Hand()
        self._wins = 0
        self._losses = 0
        if position == 'Dealer':
            print(f"{self.label} taps into table")
        elif position == 'Player':
            print(f"{self.label} sits at table")

    @property
    def hand(self):
        return self._hand

    @property
    def label(self):
        return f"{self.position} {self.name}"

    @property
    def losses(self):
        #print(f"{self.label} lost {self._losses} hands!")
        return self._losses

    @losses.setter
    def losses(self, value):
        self._losses = value

    @property
    def name(self):
        return self._name

    @property
    def position(self):
        return self._position

    @property
    def total(self):
        #print(f"{self.label} adds up hand")
        total = self.hand.value
        return total

    @property
    def wins(self):
        #print(f"{self.label} won {self._wins} hands!")
        return self._wins

    @wins.setter
    def wins(self, value):
        self._wins = value

    def doubles(self, card):
        print(f"{self.label} doubles")
        self.receives(card)
        if self.hand.value > 21:
            print(f"{self.label} Busted!")

    def hits(self, card):
        print(f"{self.label} hits")
        self.receives(card)
        if self.hand.value > 21:
            print(f"{self.label} Busted!")

    def init_hand(self):
        self._hand = Hand()

    def move(self, deck):
        result = None
        move = None
        if self.position == 'Player':
            if self.total != 21:
                while move != 'stand':
                    move = click.prompt(f"Hand total {self.total}, Your Move", default='stand')
                    if move == 'hit':
                        self.hits(deck.deal_card())
                    elif move == 'double':
                        self.doubles(deck.deal_card())
                        break
                    if self.total > 21:
                        result = 'bust'
                        break
        else:
            while self.total < 17:
                self.hits(deck.deal_card())
                if self.total > 21:
                    result = 'bust'
                    break

        print(f"{self.label}'s hand value is {self.total}")
        return result

    def receives(self, card):
        self.hand.add_card(card)
        #if self.position != 'Discard':
        #    print(f"{self.label} gets {card}")
