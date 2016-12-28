"""
Created on Dec 04, 2016

@author: john papa

Copyright 2016 John Papa.  All rights reserved.
This work is licensed under the MIT License.
"""
from abc import ABCMeta, abstractproperty

class Card(metaclass=ABCMeta):

    def __init__(self, suit, rank):
        self._rank = rank
        self._suit = suit
        self._value = None

    def __str__(self):
        return f"{self.rank} of {self.suit}"

    @property
    def rank(self):
        return self._rank

    @property
    def suit(self):
        return self._suit

    @abstractproperty
    def value(self):
        """ Returns the value of the card used for scoring the game """
