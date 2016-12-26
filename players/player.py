"""
Created on Dec 24, 2016

@author: john papa

Copyright 2016 John Papa.  All rights reserved.
This work is licensed under the MIT License.
"""
from cards.hand import Hand


class Player():

    def __init__(self, name, position='Player'):
        self._name = name
        self._position = position
        self._hand = Hand()
        if position == 'Dealer':
            print(f"{self.label} taps into table")
        else:
            print(f"{self.label} sits at table")

    @property
    def hand(self):
        return self._hand

    @property
    def label(self):
        return f"{self.position} {self.name}"

    @property
    def name(self):
        return self._name

    @property
    def position(self):
        return self._position

    @property
    def total(self):
        print(f"{self.label} adds up hand")
        total = self.hand.value
        return total

    def hits(self, card):
        print(f"{self.label} hits")
        self.receives(card)
        if self.hand.value > 21:
            print(f"{self.label} Busted!")

    def init_hand(self):
        self._hand = Hand()

    def move(self, deck):
        result = None
        while self.total < 17:
            self.hits(deck.deal_card())
        if self.total > 21:
            result = 'bust'
        return result

    def receives(self, card):
        self.hand.add_card(card)
        print(f"{self.label} gets {card}")
