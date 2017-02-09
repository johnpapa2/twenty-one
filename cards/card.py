"""
Created on Dec 04, 2016

@author: john papa

Copyright 2016 John Papa.  All rights reserved.
This work is licensed under the MIT License.
"""
from abc import ABCMeta, abstractproperty


class Card(metaclass=ABCMeta):
    """ This is an Abstract Base Class for Card objects.

    Cards from this class should work for any game played with a standard French Deck.

    """
    def __init__(self, suit, rank):
        """ Initialize the card with a rank and suit

        Arguments:
            suit - The suit of the card.
            rank - The rank of the card.
        """
        self._rank = rank
        self._suit = suit
        self._value = None

    def __str__(self):
        """ Returns a description of the card """
        return f"{self.rank} of {self.suit}"

    @property
    def rank(self):
        """ Returns the rank of the card """
        return self._rank

    @property
    def suit(self):
        """ Returns the suit of the card """
        return self._suit

    @abstractproperty
    def value(self):
        """ Returns the value of the card used for scoring the game """
