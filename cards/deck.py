"""
Created on Dec 04, 2016

@author: john papa

Copyright 2016 John Papa.  All rights reserved.
This work is licensed under the MIT License.
"""
import random

from .bjcard import BjCard


class Deck:

    def __init__(self):
        """ Initialize a standard 52 card deck in order """
        self._ranks = ['A'] + [str(n) for n in range(2, 11)] + ['J', 'Q', 'K']
        self._suits = ['spades', 'diamonds', 'clubs', 'hearts']
        self._cards = [BjCard(suit, rank) for suit in self._suits for rank in self._ranks if suit == 'spades' or suit == 'diamonds']
        self._cards += [BjCard(suit, rank) for suit in self._suits for rank in reversed(self._ranks) if suit == 'clubs' or suit == 'hearts']

    def __getitem__(self, position):
        return self._cards[position]

    def __len__(self):
        """ Return the number of cards in the deck """
        return len(self._cards)

    def deal_card(self):
        """ Remove the top card from the deck and return it """
        return self._cards.pop(0)

    def shuffle(self):
        """ Shuffle the deck """
        random.shuffle(self._cards)
