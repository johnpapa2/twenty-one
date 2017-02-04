"""
Created on Jan 15, 2017

@author: john papa

Copyright 2017 John Papa.  All rights reserved.
This work is licensed under the MIT License.
"""


class Bet():
    """ This is a class for Bets used in the game of Blackjack.

    Bets from this class should work for any standard game of blackjack or twenty-one.

    """
    def __init__(self, value=0):
        """ Initialize the bet to a given amount

        Arguments:
            value - The amount of the bet, placed before the hand is dealt.
        """
        self._amount = value

    @property
    def amount(self):
        """ Return the amount of the bet """
        return self._amount

    @amount.setter
    def amount(self, value):
        """ Set the amount of the bet

        Arguments:
            value - The new amount to set the bet to.
        """
        self._amount = value

    def increase(self, additional_bet):
        """ Add more money to the initial amount bet

        Arguments:
            additional_bet - The amount to add to the existing bet.
        """
        self._amount += additional_bet
