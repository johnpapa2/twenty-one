"""
Created on Dec 24, 2016

@author: john papa

Copyright 2016 John Papa.  All rights reserved.
This work is licensed under the MIT License.
"""

class Hand:

    def __init__(self):
        self._cards = list()

    def __getitem__(self, position):
        return self._cards[position]

    def __len__(self):
        """ Return the number of cards in the hand """
        return len(self._cards)

    def add_card(self, card):
        """ Add a card to the hand """
        self._cards.append(card)
