"""
Created on Dec 24, 2016

@author: john papa

Copyright 2016 John Papa.  All rights reserved.
This work is licensed under the MIT License.
"""


class Hand:

    def __init__(self):
        self._cards = list()
        self._bet = 0

    def __getitem__(self, position):
        return self._cards[position]

    def __len__(self):
        """ Return the number of cards in the hand """
        return len(self._cards)

    def __str__(self):
        """ Display the hand on the command line """
        ranks = [card.rank for card in self._cards]
        hand = '] ['.join(ranks)
        return (f"[{hand}]")

    @property
    def bet(self):
        return self._bet

    @bet.setter
    def bet(self, value):
        self._bet = value

    def add_card(self, card):
        """ Add a card to the hand """
        self._cards.append(card)

    @property
    def value(self):
        """ Return the value of the hand """
        value = sum(card.value for card in self._cards)
        if value < 21:
            for card in self._cards:
                if card.rank == 'A' and value <= 11:
                    value += 10
        return value
