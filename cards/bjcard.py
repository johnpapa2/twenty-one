"""
Created on Dec 24, 2016

@author: john papa

Copyright 2016 John Papa.  All rights reserved.
This work is licensed under the MIT License.
"""
from .card import Card

class BjCard(Card):

    def __init__(self, *args, **kwarg):
        super().__init__(*args, **kwarg)

    @property
    def value(self):
        """ Returns the value of the card used for scoring the game """
        if self._value:
            return self._value
        elif self.rank not in list('JQKA'):
            self._value = int(self.rank)
        elif self.rank in list('JQK'):
            self._value = 10
        else:
            self._value = 11
        return self._value
