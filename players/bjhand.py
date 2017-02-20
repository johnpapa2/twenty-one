"""
Created on Dec 24, 2016

@author: john papa

Copyright 2016 John Papa.  All rights reserved.
This work is licensed under the MIT License.
"""
import db
import logging

from .hand import Hand
from .bet import Bet


class BjHand(Hand):
    """ This is a class for Hands used in the game of Blackjack.

    Hands from this class should work for any standard game of blackjack or twenty-one.

    """
    def __init__(self, session, player_id, bet):
        """ Initialize the hand as an empty list of cards and a bet

        Arguments:
            bet - The amount to bet before recieving cards for the hand
        """
        super().__init__()
        self._session = session
        self._bet = Bet(bet)
        self._blackjack = None
        self._db_info = db.Hand(bet=bet, player_id=player_id)
        self._session.add(self._db_info)
        self._session.commit()
        self._logger = logging.getLogger('bj')

    @property
    def bet(self):
        """ Returns the bet associated with this hand """
        return self._bet

    @property
    def can_split(self):
        """ Checks to see if a hand can be split into two hands """
        splittable = False
        if len(self) == 2:
            if self.cards[0].value == self.cards[1].value:
                splittable = True
        return splittable

    @property
    def db_info(self):
        """ Returns the db info associated with this hand """
        return self._db_info

    @property
    def is_blackjack(self):
        """ Checks to see if the hand is a Natural Blackjack """
        if self._blackjack:
            return self._blackjack
        else:
            if len(self) == 2 and self.value == 21:
                self._blackjack = True
            else:
                self._blackjack = False
        self._db_info.is_blackjack = self._blackjack
        return self._blackjack

    @property
    def value(self):
        """ Return the value of the hand """
        value = sum(card.value for card in self.cards)
        if value > 21:
            for card in self.cards:
                if card.rank == 'Ace' and card.value == 11:
                    card.set_ace_low()
                    value = sum(card.value for card in self.cards)
                if value <= 21:
                    break
        return value
