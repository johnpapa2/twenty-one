"""
Created on Dec 24, 2016

@author: john papa

Copyright 2016 John Papa.  All rights reserved.
This work is licensed under the MIT License.
"""
import db
import logging

from .card import Card


class BjCard(Card):
    """ This is a class for Cards used in the game of Blackjack.

    Cards from this class should work for any standard game of blackjack or twenty-one.

    """
    def __init__(self, session, suit, rank):
        """ Initialize the card with a rank and suit

        Arguments:
            suit - The suit of the card. Allowed values are 'spades', 'diamonds', 'clubs', or 'hearts'.
            rank - The rank of the card. Allowed values are 'A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K'.
        """
        super().__init__(suit, rank)
        self._session = session
        self._logger = logging.getLogger('bj')

    @property
    def value(self):
        """ Returns the value of the card based on a standard game of Blackjack """
        # ranks = [rank.name for rank in self._session.query(db.Rank).all()]
        face_ranks = ['Jack', 'Queen', 'King']
        ace_rank = 'Ace'
        if self._value:
            return self._value
        elif self.rank not in (face_ranks + [ace_rank]):
            self._value = int(self.rank)
        elif self.rank in face_ranks:
            self._value = 10
        elif self.rank == ace_rank:
            self._value = 11
        self._logger.info(f"My {self} is worth {self._value} points")
        return self._value

    def set_ace_low(self):
        """ Set the value of an Ace to 1 """
        if self.rank == 'Ace':
            self._value = 1
