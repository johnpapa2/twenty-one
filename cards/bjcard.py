"""
Created on Dec 24, 2016

@author: john papa

Copyright 2016 John Papa.  All rights reserved.
This work is licensed under the MIT License.
"""
import logging

from .card import Card


class BjCard(Card):
    """ This is a class for Cards used in the game of Blackjack.

    Cards from this class should work for any standard game of blackjack or twenty-one.

    """
    def __init__(self, suit, rank):
        """ Initialize the card with a rank and suit

        Arguments:
            suit - The suit of the card. Allowed values are 'spades', 'diamonds', 'clubs', or 'hearts'.
            rank - The rank of the card. Allowed values are 'A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K'.
        """
        super().__init__(suit, rank)
        self._logger = logging.getLogger('bj')

    @property
    def value(self):
        """ Returns the value of the card based on a standard game of Blackjack """
        if self._value:
            return self._value
        elif self.rank not in list('JQKA'):
            self._value = int(self.rank)
        elif self.rank in list('JQK'):
            self._value = 10
        elif self.rank == 'A':
            self._value = 11
        self._logger.debug(f"My {self} is worth {self._value} points")
        return self._value

    def set_ace_low(self):
        """ Set the value of an Ace to 1 """
        if self.rank == 'A':
            self._value = 1
