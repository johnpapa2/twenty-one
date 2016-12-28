"""
Created on Dec 24, 2016

@author: john papa

Copyright 2016 John Papa.  All rights reserved.
This work is licensed under the MIT License.
"""
import logging

from .card import Card

class BjCard(Card):

    def __init__(self, suit, rank):
        super().__init__(suit, rank)
        self._logger = logging.getLogger('bj')

    @property
    def value(self):
        """ Returns the value of the card used for scoring the game """
        if self._value:
            return self._value
        elif self.rank not in list('JQKA'):
            self._value = int(self.rank)
        elif self.rank in list('JQK'):
            self._value = 10
        elif self.rank == 'A':
            self._value = 1
        self._logger.debug(f"My {self} is worth {self._value} points")
        return self._value
