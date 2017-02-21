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
    def __init__(self, session, name):
        """ Initialize the strategy.

        Arguments:
            none
        """
        self._session = session
        self._db_info = self._session.query(db.Strategy).filter_by(name=name).one()
        self._logger = logging.getLogger('bj')
        self._actions = {action.name: action.id for action in self._session.query(db.Action).all()}
        self._deck_of_cards = {card.name: card.id for card in self._session.query(db.Card).all()}
        self._name = name

    @property
    def db_info(self):
        """ Returns the db object associated with this hand """
        return self._db_info

    @property
    def name(self):
        return self._name

    def decision(self, hand, upcard, count=None):
        if self.name == 'no_bust':
            if hand.value < 11 or (hand.is_soft and hand.value < 18):
                print(f"Strategy aginst dealer upcard >- {upcard} -< with {hand} is HIT")
                action = 'hit'
            else:
                print(f"Strategy aginst dealer upcard >- {upcard} -< with {hand} is STAND")
                action = 'stand'
        elif self.name == 'mimic_dealer':
            if hand.value < 17 or (hand.is_soft and hand.value < 18):
                print(f"Strategy aginst dealer upcard >- {upcard} -< with {hand} is HIT")
                action = 'hit'
            else:
                print(f"Strategy aginst dealer upcard >- {upcard} -< with {hand} is STAND")
                action = 'stand'
        elif self.name == 'stand':
            print(f"Strategy aginst dealer upcard >- {upcard} -< with {hand} is STAND")
            action = 'stand'
        return action
