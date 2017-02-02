"""
Created on Dec 24, 2016

@author: john papa

Copyright 2016 John Papa.  All rights reserved.
This work is licensed under the MIT License.
"""
import logging

from .hand import Hand
from .bet import Bet


class BjHand(Hand):

    def __init__(self):
        super().__init__()
        self.bet = Bet()
        self._blackjack = None
        self._logger = logging.getLogger('bj')

    @property
    def is_blackjack(self):
        if self._blackjack:
            return self._blackjack
        else:
            if len(self) == 2 and self.value == 21:
                self._blackjack = True
            else:
                self._blackjack = False
        return self._blackjack

    @property
    def value(self):
        """ Return the value of the hand """
        value = sum(card.value for card in self._cards)
        if value > 21:
            for card in self._cards:
                if card.rank == 'A' and card.value == 11:
                    card.set_ace_low()
                    value = sum(card.value for card in self._cards)
                if value <= 21:
                    break
        return value
