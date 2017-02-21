"""
Created on Feb 20, 2017

@author: john papa

Copyright 2017 John Papa.  All rights reserved.
This work is licensed under the MIT License.
"""
import db
import logging


class Strategy():
    """ This is a class for Strategy used in the game of Blackjack.

    """
    def __init__(self, session):
        """ Initialize the strategy.

        Arguments:
            none
        """
        self._session = session
        self._logger = logging.getLogger('bj')
        self._actions = {action.name: action.id for action in self._session.query(db.Action).all()}
        self._deck_of_cards = {card.name: card.id for card in self._session.query(db.Card).all()}

    def decision(self, hand, upcard, count=None):
        if hand.value < 11 or (hand.is_soft and hand.value < 18):
            print(f"Strategy aginst dealer upcard >- {upcard} -< with {hand} is HIT")
            action = 'hit'
        else:
            print(f"Strategy aginst dealer upcard >- {upcard} -< with {hand} is STAND")
            action = 'stand'
        return action
