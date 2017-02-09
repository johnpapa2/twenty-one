"""
Created on Jan 16, 2017

@author: john papa

Copyright 2017 John Papa.  All rights reserved.
This work is licensed under the MIT License.
"""


class Bankroll():
    """ This is a class for Bankrolls used in the game of Blackjack or other gambling games.

    Bankrolls from this class should work for any game that requires a bankroll.

    """
    def __init__(self, value=0):
        """ Initialize the bankroll to a given amount

        Arguments:
            value - The amount of the bankroll to start with.
        """
        self._amount = value

    @property
    def amount(self):
        """ Return the amount of the bankroll """
        return self._amount

    @amount.setter
    def amount(self, value):
        """ Set the amount of the bankroll

        Arguments:
            value - The new amount to set the bankroll to.
        """
        self._amount = value

    def invest(self, investment):
        """ Add more money to the amount in the bankroll

        Arguments:
            investment - The amount to add to the existing bankroll.
        """
        self._amount += investment

    def withdraw(self, withdrawl):
        """ Take money out of the amount in the bankroll

        Arguments:
            withdrawl - The amount to remove from the existing bankroll.
        """
        self._amount -= withdrawl
